#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services


def run(ic, args):
    proxy = ic.stringToProxy(args[1])
    container = Services.ContainerPrx.checkedCast(proxy)

    if not container:
        raise RuntimeError('Invalid proxy')

    print(container.list())

    return 0


if __name__ == '__main__':
    with Ice.initialize(sys.argv) as communicator:
        sys.exit(run(communicator, sys.argv))
