#!/usr/bin/env -S python3 -u

import sys
import time
import Ice
Ice.loadSlice('printer.ice')
import Example


def main(ic):
    proxy = ic.stringToProxy(sys.argv[1])
    printer = Example.PrinterPrx.uncheckedCast(proxy)

    if not printer:
        raise RuntimeError('Invalid proxy')

    while 1:
        try:
            printer.write('Hello World!')
            print('invocation succed')

        except Ice.NotRegisteredException:
            print('invocation FAILED')

        time.sleep(1)


if __name__ == "__main__":
    with Ice.initialize() as communicator:
        main(communicator)
