#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('-I. --all PrinterFactory.ice')
import Example


class PrinterI(Example.Printer):
    def __init__(self, name):
        self.name = name

    def write(self, message, current=None):
        print("{0}: {1}".format(self.name, message))
        sys.stdout.flush()


class PrinterFactoryI(Example.PrinterFactory):
    def make(self, name, current=None):
        servant = PrinterI(name)
        proxy = current.adapter.addWithUUID(servant)
        return Example.PrinterPrx.checkedCast(proxy)


def run(ic):
    servant = PrinterFactoryI()

    adapter = ic.createObjectAdapter("PrinterFactoryAdapter")
    proxy = adapter.add(servant, ic.stringToIdentity("printerFactory1"))

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
