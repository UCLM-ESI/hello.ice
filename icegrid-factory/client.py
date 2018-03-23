#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I. --all factory.ice')
Ice.loadSlice('-I. --all printer.ice')

import Example  # noqa


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        factory = Example.FactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError('Invalid proxy')

        proxy = factory.make("printer1")
        printer = Example.PrinterPrx.checkedCast(proxy)

        printer.write('Hello World!')

        return 0


sys.exit(Client().main(sys.argv))
