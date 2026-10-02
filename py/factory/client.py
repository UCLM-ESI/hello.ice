#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('-I. --all PrinterFactory.ice')
import Example


def run(ic, args):
    proxy = ic.stringToProxy(args[1])
    factory = Example.PrinterFactoryPrx.checkedCast(proxy)
    if not factory:
        raise RuntimeError('Invalid proxy')

    printer = factory.make("printer1")
    printer.write('Hello World!')

    return 0


if __name__ == '__main__':
    with Ice.initialize(sys.argv) as communicator:
        sys.exit(run(communicator, sys.argv))
