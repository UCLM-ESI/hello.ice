#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('factorial.ice')
import Example


# NOTE: this example uses the deprecated begin_/end_ AMI API, kept only for
# reference. Use the <operation>Async() methods instead, which return a future
# (see client-block.py, client-callback.py and client-await.py).

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        math = Example.MathPrx.checkedCast(proxy)

        if not math:
            raise RuntimeError("Invalid proxy")

        async_result = math.begin_factorial(int(argv[2]))
        print('that was an async call')

        print(math.end_factorial(async_result))

        return 0


if len(sys.argv) != 3:
    print(f"usage: {__file__} <server> <value>")
    sys.exit(1)

app = Client()
sys.exit(app.main(sys.argv))
