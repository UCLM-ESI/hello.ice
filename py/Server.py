#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys, Ice
Ice.loadSlice('Hello.ice')
import Example


class HelloI(Example.Hello):
    def puts(self, s, current=None):
        print s


class Server(Ice.Application):
    def run(self, argv):
        ic = self.communicator()

        oa = ic.createObjectAdapter("HelloAdapter")
        base = oa.add(HelloI(), ic.stringToIdentity("hello1"))
        oa.activate()

        print base

        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
