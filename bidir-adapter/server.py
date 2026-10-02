#!/usr/bin/env -S python3 -u

import sys
import Ice
from pathlib import Path

Ice.loadSlice('-I{} {}'.format(Ice.getSliceDir(), Path(__file__).parent / 'BidirAdapter.ice'))
import Utils


class MessageForwarder(Ice.Blobject):
    def __init__(self, peer, adapter):
        self.peer = peer
        self.adapter = adapter

    def ice_invoke(self, in_params, current):
        try:
            print(" - forward to '{}'".format(self.peer.ice_getIdentity().name))
            return self.peer.ice_invoke(
                current.operation, current.mode, in_params, current.ctx)
        except Ice.Exception as e:
            msg = "  : ERROR: "
            msg += "> " + str(e).replace("\n", "\n" + " " * len(msg) + "> ")
            print(msg)

            self.discard()
            return True, bytes()

    def discard(self):
        oid = self.peer.ice_getIdentity()
        print("  : discarding proxy: {}...".format(oid.name))
        try:
            self.adapter.remove(oid)
        except Ice.NotRegisteredException:
            pass


class BidirAdapterI(Utils.BidirAdapter):
    def __init__(self, adapter):
        self.adapter = adapter

    def add(self, peer, current):
        oid = peer.ice_getIdentity()
        peer = current.con.createProxy(oid)
        servant = MessageForwarder(peer, self.adapter)

        try:
            return self.adapter.add(servant, oid)
        except Ice.AlreadyRegisteredException:
            self.adapter.remove(oid)
            return self.adapter.add(servant, oid)

    def getproxy(self, identity):
        return self.adapter.find(identity)


def main(ic):
    adapter = ic.createObjectAdapter("Adapter")

    servant = BidirAdapterI(adapter)
    proxy = adapter.add(servant, ic.stringToIdentity("bidir-adapter"))
    print(proxy)

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("\nShutting down server...")
