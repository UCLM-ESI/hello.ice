#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import Ice
Ice.loadSlice('./factorial.ice')
import Example


def factorialCB(value):
    print "Value is: %s" % value


def failureCB(ex):
    print "Exception is: " + str(ex)


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        math = Example.MathPrx.checkedCast(proxy)

        if not math:
            raise RuntimeError("Invalid proxy")

        math.begin_factorial(argv[2], factorialCB, failureCB)
        print 'this was an async call'

        return 0


if len(sys.argv) != 3:
    print __doc__.format(__file__)
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
