#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, Ice
Ice.loadSlice('ami.ice')
import Demo


class client (Ice.Application):

    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])

        prx = Demo.EmployeesPrx.checkedCast(base)

        if not prx:
            raise RuntimeError("Invalid proxy")

        async_result = prx.begin_getName(1)
        print 'this was a async call'

        print prx.end_getName(async_result)

        return 0


sys.exit(client().main(sys.argv))
