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


class PrinterFactoryI(Example.PrinterFactory):
    def __init__(self):
        self.objects = {}

    def make(self, name, current=None):
        if name in self.objects:
            return self.objects[name]

        print(f"Creating new printer: '{name}'")

        servant = PrinterI(name)
        proxy = current.adapter.addWithUUID(servant)
        printer = self.objects[name] = Example.PrinterPrx.checkedCast(proxy)

        return printer


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
