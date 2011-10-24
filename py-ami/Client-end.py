#!/usr/bin/python
# -*- coding: utf-8 -*-
"usage: {} <server> <value>"

import sys, Ice
Ice.loadSlice('../factorial.ice')
import UCLM


class Client(Ice.Application):
    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])

        prx = UCLM.MathPrx.checkedCast(base)

        if not prx:
            raise RuntimeError("Invalid proxy")

        async_result = prx.begin_factorial(argv[2])
        print 'this was a async call'

        print prx.end_factorial(async_result)

        return 0


if len(sys.argv) != 3:
    print __doc__.format(__file__)
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
