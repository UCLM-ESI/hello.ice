#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('factorial.ice')
import Example


def factorial(n):
    if n < 0:
        raise ValueError(f"wrong arg value: {n}")
    if n in [0, 1]:
        return 1
    return n * factorial(n - 1)


class MathI(Example.Math):
    def factorial(self, value, current=None):
        print(f"Received request for factorial({value})")
        return factorial(value)


def main(ic):
    servant = MathI()
    adapter = ic.createObjectAdapter("MathAdapter")
    proxy = adapter.add(servant, ic.stringToIdentity("math1"))

    print(proxy)

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("\nShutting down server...")
