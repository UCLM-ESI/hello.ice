#!/usr/bin/env python
# -*- coding: utf-8; mode: python; -*-

import sys
import Ice

Ice.loadSlice('Printer.ice')
Ice.loadSlice('-I{} Callback.ice'.format(Ice.getSliceDir()))
import Example


class PrinterI(Example.Printer):
    n = 1

    def write(self, message, current=None):
        print("{0}: {1}".format(self.n, message))
        sys.stdout.flush()
        self.n += 1


class Client(Ice.Application):
    # This is a Callback client, but also a Printer server

    def run(self, argv):
        broker = self.communicator()

        servant = PrinterI()
        identity = Ice.Identity(Ice.generateUUID())

        adapter = broker.createObjectAdapter("")
        adapter.add(servant, identity)
        adapter.activate()

        proxy = broker.stringToProxy(argv[1])
        server = Example.CallbackPrx.checkedCast(proxy)
        server.ice_getConnection().setAdapter(adapter)
        server.attach(identity)

        self.communicator().waitForShutdown()
        return 0


sys.exit(Client().main(sys.argv))
