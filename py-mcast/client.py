#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('printer.ice')
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        printer = Example.PrinterPrx.uncheckedCast(proxy.ice_datagram())

        if not printer:
            raise RuntimeError('Invalid proxy')

        printer.write('Hello World!')

        return 0


sys.exit(Client().main(sys.argv))
