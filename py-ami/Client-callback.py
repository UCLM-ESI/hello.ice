#!/usr/bin/env -S python3 -u

import sys

import Ice
Ice.loadSlice('./factorial.ice')
import Example


class Client(Ice.Application):
    def callback(self, future):
        try:
            print(f"Callback: value is: {future.result()}")
        except Exception as ex:
            print(f"Exception is: {ex}")

    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        math = Example.MathPrx.checkedCast(proxy)
        value = int(argv[2])

        if not math:
            raise RuntimeError("Invalid proxy")

        future = math.factorialAsync(value)
        future.add_done_callback(self.callback)

        print("That was an async call")
        return 0


if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
