#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import Ice
Ice.loadSlice('Printer.ice')
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        printer = Example.PrinterPrx.uncheckedCast(proxy)

        if not printer:
            raise RuntimeError('Invalid proxy')

        while 1:
            try:
                printer.write('Hello World!')
                print('invocatión succed')
            except Ice.NotRegisteredException:
                print('invocation FAILED')
            time.sleep(1)

        return 0


sys.exit(Client().main(sys.argv))
