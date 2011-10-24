#!/usr/bin/python
# -*- coding: utf-8 -*-
"usage: {} <server> <value>"

import sys, Ice
Ice.loadSlice('../factorial-amd.ice')
import UCLM


class Client(Ice.Application):

    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])

        prx = UCLM.MathPrx.checkedCast(base)

        if not prx:
            raise RuntimeError("Invalid proxy")

        print prx.factorial(int(argv[2]))

        return 0


if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)


app = Client()
sys.exit(app.main(sys.argv))
