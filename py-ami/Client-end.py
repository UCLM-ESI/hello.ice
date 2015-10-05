#!/usr/bin/python
# -*- coding: utf-8 -*-
"usage: {} <server> <value>"

import sys
import Ice
Ice.loadSlice('./factorial.ice')
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        math = Example.MathPrx.checkedCast(proxy)

        if not math:
            raise RuntimeError("Invalid proxy")

        async_result = math.begin_factorial(int(argv[2]))
        print 'that was an async call'

        print math.end_factorial(async_result)

        return 0


if len(sys.argv) != 3:
    print __doc__.format(__file__)
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
