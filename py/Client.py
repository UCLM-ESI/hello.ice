#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, Ice
Ice.loadSlice('Hello.ice')
import Example


class client (Ice.Application):

    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])

        prx = Example.HelloPrx.checkedCast(base)

        if not prx:
            raise RuntimeError("Invalid proxy")

        prx.puts("Hello World!")

        return 0


sys.exit(client().main(sys.argv))
