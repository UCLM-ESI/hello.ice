#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I. --all factory.ice')
Ice.loadSlice('-I. --all printer.ice')

import IceCloud  # noqa
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        factory = IceCloud.FactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError('Invalid proxy')

        proxy = factory.make('node1', 'PrinterTemplate',
                             {'name': 'printer1'})
        printer = Example.PrinterPrx.checkedCast(proxy)

        printer.write('Hello World!')

        return 0


sys.exit(Client().main(sys.argv))
