#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    n = 0

    def write(self, message, current=None):
        print("{0}: {1}".format(self.n, message))
        sys.stdout.flush()
        self.n += 1


def main(ic):
    servant = PrinterI()
    adapter = ic.createObjectAdapter("PrinterAdapter")
    proxy = adapter.add(servant, ic.stringToIdentity("printer1"))

    print(proxy)

    adapter.activate()
    ic.waitForShutdown()


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("\nShutting down server...")
