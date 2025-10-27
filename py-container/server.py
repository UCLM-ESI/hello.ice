#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services


class ContainerI(Services.Container):
    def __init__(self):
        self.proxies = dict()

    def link(self, key, proxy, current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies


def run(ic):
    servant = ContainerI()

    adapter = ic.createObjectAdapter("ContainerAdapter")
    proxy = adapter.add(servant, ic.stringToIdentity("container1"))

    print(proxy)

    adapter.activate()
    ic.waitForShutdown()

    return 0


if __name__ == '__main__':
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(run(communicator))
    except KeyboardInterrupt:
        print("\nShutting down server...")
