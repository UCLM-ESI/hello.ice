#!/usr/bin/env -S python3 -u

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
    print(f"usage: {__file__} <server> <value>")
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
