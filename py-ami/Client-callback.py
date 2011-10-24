#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, Ice
Ice.loadSlice('../ami.ice')
import UCLM


def factorialCB(name):
    print "Name is: " + name


def failureCB(ex):
    print "Exception is: " + str(ex)


class Client(Ice.Application):

    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])

        prx = UCLM.MathPrx.checkedCast(base)

        if not prx:
            raise RuntimeError("Invalid proxy")

        prx.begin_factorial(argv[2], factorialCB, failureCB)
        print 'this was a async call'

        return 0


if len(sys.argv) != 3:
    print __doc__.format(__file__)
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
