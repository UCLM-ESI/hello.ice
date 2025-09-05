#!/usr/bin/env -S python3 -u

import sys

import Ice
Ice.loadSlice('factorial.ice')
import Example


class Client(Ice.Application):

    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])
        math = Example.MathPrx.checkedCast(base)

        if not math:
            raise RuntimeError("Invalid proxy")

        print(math.factorial(int(argv[2])))

        return 0


if len(sys.argv) != 3:
    print(f"usage: {__file__} <server> <value>")
    sys.exit(1)


app = Client()
sys.exit(app.main(sys.argv))
