#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I. --all factory.ice')
Ice.loadSlice('-I. --all printer.ice')

import Generic  # noqa
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        factory = Generic.FactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError('Invalid proxy')

        proxy = factory.make('node1', 'PrinterTemplate', 'printer1')
        printer = Example.PrinterPrx.checkedCast(proxy)

        printer.write('Hello World!')

        return 0


sys.exit(Client().main(sys.argv))
