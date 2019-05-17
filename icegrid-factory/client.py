#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import time

Ice.loadSlice('-I. --all factory.ice')
Ice.loadSlice('-I. --all printer.ice')

import IceCloud  # noqa
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        factory = self.retry_cast(IceCloud.ServerFactoryPrx, proxy)

        proxy = factory.make('node1', 'PrinterTemplate', {'name': 'printer1'})
        printer = self.retry_cast(Example.PrinterPrx, proxy)

        printer.write('Hello World!')
        print('ok')

    def retry_cast(self, cast, proxy):
        for i in range(5):
            try:
                retval = cast.checkedCast(proxy)
                break
            except Ice.ObjectNotExistException:
                print('.', end='')
                time.sleep(0.5)
            else:
                raise Exception("Object '{}' not available".format(proxy))

        if not retval:
            raise RuntimeError("Invalid proxy: '{}'".format(proxy))

        return retval

sys.exit(Client().main(sys.argv))
