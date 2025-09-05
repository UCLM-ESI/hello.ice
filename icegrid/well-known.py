#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy('printer1')
        printer = Example.PrinterPrx.checkedCast(proxy)

        if not printer:
            raise RuntimeError('Invalid proxy')

        printer.write('Hello World!')

        return 0


sys.exit(Client().main(sys.argv))
