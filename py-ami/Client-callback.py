#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import Ice
Ice.loadSlice('./factorial.ice')
import Example


class FactorialCB(object):
    def response(self, retval):
        print("Callback: Value is {}".format(retval))

    def failure(self, ex):
        print("Exception is: {}".format(ex))


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        math = Example.MathPrx.checkedCast(proxy)

        if not math:
            raise RuntimeError("Invalid proxy")

        factorial_cb = FactorialCB()

        math.begin_factorial(int(argv[2]),
                             factorial_cb.response, factorial_cb.failure)
        print 'that was an async call'

        return 0


if len(sys.argv) != 3:
    print __doc__.format(__file__)
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
