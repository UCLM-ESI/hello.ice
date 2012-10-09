#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
import IceGrid

Ice.loadSlice('Printer.ice')
import Example


class client(Ice.Application):
    def get_query(self):
        proxy = self.communicator().stringToProxy('IceGrid/Query')
        return IceGrid.QueryPrx.checkedCast(proxy)

    def run(self, argv):
        query = self.get_query()

        if not query:
            raise RuntimeError('Invalid proxy')

        proxy = query.findObjectByType('::Example::Printer')
        printer = Example.PrinterPrx.checkedCast(proxy)
        printer.write('Hello World!')

        return 0


sys.exit(client().main(sys.argv))
