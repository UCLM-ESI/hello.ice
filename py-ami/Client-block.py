#!/usr/bin/env -S python3 -u
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
        value = int(argv[2])

        if not math:
            raise RuntimeError("Invalid proxy")

        future = math.factorialAsync(value)
        print("That was an async call")

        print(f"Async result is: {future.result()}")

        return 0


if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
