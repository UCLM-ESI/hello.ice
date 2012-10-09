#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print message


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PrinterI()

        adapter = broker.createObjectAdapter("PrinterAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("printer1"))

        print proxy

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
