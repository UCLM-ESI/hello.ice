#!/usr/bin/env -S python3 -u

import sys
import Ice

Ice.loadSlice('DocPrinter.ice')
import Example
from Doc_pb2 import Doc


class Client(Ice.Application):
    def run(self, args):
        proxy = self.communicator().stringToProxy(args[1])
        printer = Example.DocPrinterPrx.checkedCast(proxy)

        if not printer:
            raise RuntimeError('Invalid proxy')

        m = Doc()
        m.data = "Hello World!"
        m.user = "john.doe@example.com"

        printer.write(m)

        return 0

sys.exit(Client().main(sys.argv))
