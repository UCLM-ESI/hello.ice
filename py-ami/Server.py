#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys, Ice
import time
Ice.loadSlice('../factorial.ice')
import UCLM


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


class MathI(UCLM.Math):
    def factorial(self, n, current=None):
        return str(factorial(n))


class Server(Ice.Application):
    def run(self, argv):
        ic = self.communicator()

        oa = ic.createObjectAdapter("OA")
        base = oa.add(MathI(), ic.stringToIdentity("hello1"))
        oa.activate()

        print base

        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
