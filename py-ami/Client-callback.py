#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, Ice
Ice.loadSlice('ami.ice')
import Demo


def getNameCB(name):
    print "Name is: " + name


def failureCB(ex):
    print "Exception is: " + str(ex)


class client (Ice.Application):

    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])

        prx = Demo.EmployeesPrx.checkedCast(base)

        if not prx:
            raise RuntimeError("Invalid proxy")

        prx.begin_getName(1, getNameCB, failureCB)
        print 'this was a async call'

        return 0


sys.exit(client().main(sys.argv))
