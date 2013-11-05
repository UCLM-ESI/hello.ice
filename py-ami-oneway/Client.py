#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

import Ice
Ice.loadSlice('Printer.ice')
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        proxy = proxy.ice_oneway()
        printer = Example.PrinterPrx.uncheckedCast(proxy)

        if not printer:
            raise RuntimeError('Invalid proxy')

        handler = printer.begin_write('Hello World!')

        # polling for sent
        while not handler.isSent():
            time.sleep(0.1)

        return 0


sys.exit(Client().main(sys.argv))
