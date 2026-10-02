#!/usr/bin/env -S python3 -u

import sys
import time
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'factorial.ice'))
import Example


def main(ic):
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <proxy> <value>")
        return 1

    proxy = ic.stringToProxy(sys.argv[1])
    math = Example.MathPrx.checkedCast(proxy)
    value = int(sys.argv[2])

    if not math:
        raise RuntimeError('Invalid proxy')

    future = math.factorialAsync(value)

    while not future.done():
        print("Still waiting...")
        time.sleep(0.1)

    print(f"Async result is: {future.result()}")

    return 0


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        sys.exit(main(communicator))
