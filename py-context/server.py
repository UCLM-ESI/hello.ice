#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print("msg: '{}', context: {}".format(message, current.ctx))
        sys.stdout.flush()


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PrinterI()

        adapter = broker.createObjectAdapter("PrinterAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("printer1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
