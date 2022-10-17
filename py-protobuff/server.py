#!/usr/bin/python3 -u


import sys
import Ice

Ice.loadSlice('DocPrinter.ice')
import Example
from Doc_pb2 import Doc


class PrinterI(Example.DocPrinter):
    def write(self, p, current=None):
        print(p)


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = PrinterI()

        adapter = broker.createObjectAdapter("PrinterAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("printer1"))

        # print(proxy, flush=True)
        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))