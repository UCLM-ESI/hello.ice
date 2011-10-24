#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys, Ice
import time
Ice.loadSlice('ami.ice')
import Demo


class DemoI(Demo.Employees):
    def getName(self, key, current=None):
        print('-> getName({})'.format(key))
        time.sleep(1)
        return "John Doe"


class Server(Ice.Application):
    def run(self, argv):
        ic = self.communicator()

        oa = ic.createObjectAdapter("OA")
        base = oa.add(DemoI(), ic.stringToIdentity("hello1"))
        oa.activate()

        print base

        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
