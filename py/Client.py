#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Hello.ice')
import Example


class client (Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        hello = Example.HelloPrx.checkedCast(proxy)

        if not hello:
            raise RuntimeError("Invalid proxy")

        hello.puts("Hello World!")

        return 0


sys.exit(client().main(sys.argv))
