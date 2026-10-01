#!/usr/bin/env -S python3 -u

import sys
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'factorial.ice'))
import Example


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


class MathI(Example.Math):
    def factorial(self, n, current=None):
        return factorial(n)


def main(ic):
    adapter = ic.createObjectAdapter("MathAdapter")
    proxy = adapter.add(MathI(), Ice.stringToIdentity("math1"))

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
