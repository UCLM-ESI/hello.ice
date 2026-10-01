#!/usr/bin/env -S python3 -u

import sys
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'factorial.ice'))
import Example


def callback(future):
    try:
        print(f"Callback: value is: {future.result()}")
    except Exception as ex:
        print(f"Exception is: {ex}")


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
    future.add_done_callback(callback)

    print("That was an async call")

    return 0


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        sys.exit(main(communicator))
