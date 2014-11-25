#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all PrinterFactory.ice')
import Example


class PrinterI(Example.Printer):
    def __init__(self, name):
        self.name = name

    def write(self, message, current=None):
        print("{0}: {1}".format(self.name, message))
        sys.stdout.flush()


class PrinterFactoryI(Example.PrinterFactory):
    def make(self, name, current=None):
        servant = PrinterI(name)
        proxy = current.adapter.addWithUUID(servant)
        return Example.PrinterPrx.checkedCast(proxy)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PrinterFactoryI()

        adapter = broker.createObjectAdapter("PrinterFactoryAdapter")
        proxy = adapter.add(servant,
                            broker.stringToIdentity("printerFactory1"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
