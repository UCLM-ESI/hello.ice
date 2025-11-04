#!/usr/bin/env -S python3 -u

import sys
import Ice
from uuid import uuid4
from Ice import identityToString as id2str, stringToIdentity as str2id
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    def __init__(self, identities):
        super().__init__()
        self.valid_identities = set(identities)

    def ensure_valid_object(self, identity):
        if identity.name not in self.valid_identities:
            raise Ice.ObjectNotExistException()

    def ice_ping(self, current=None):
        self.ensure_valid_object(current.id)

    def write(self, message, current=None):
        self.ensure_valid_object(current.id)
        print(f"{id2str(current.id)}: {message}")


def main(ic):
    identities = [f'printer-{uuid4().hex[:8]}' for _ in range(20)]
    servant = PrinterI(identities)

    adapter = ic.createObjectAdapter('PrinterAdapter')
    adapter.addDefaultServant(servant, category='')

    for identity in identities:
        print(adapter.createDirectProxy(str2id(identity)))

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        pass
