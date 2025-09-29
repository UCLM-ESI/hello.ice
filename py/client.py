#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('printer.ice')
import Example


def main(ic):
    proxy = ic.stringToProxy(sys.argv[1])
    printer = Example.PrinterPrx.checkedCast(proxy)

    if not printer:
        raise RuntimeError('Invalid proxy')

    printer.write('Hello World!')


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
