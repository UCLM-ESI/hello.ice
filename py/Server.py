#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Hello.ice')
import Example


class HelloI(Example.Hello):
    def puts(self, s, current=None):
        print s


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = HelloI()

        adapter = broker.createObjectAdapter("HelloAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("hello1"))

        print proxy

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
