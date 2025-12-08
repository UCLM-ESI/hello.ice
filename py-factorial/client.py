#!/usr/bin/env -S python3 -u

import sys
import Ice
Ice.loadSlice('factorial.ice')
import Example


def main(ic):
    proxy = ic.stringToProxy(sys.argv[1])
    math = Example.MathPrx.checkedCast(proxy)

    if not math:
        raise RuntimeError('Invalid proxy')

    for value in [0, 5, 7]:
        result = math.factorial(value)
        print(f"factorial({value}) = {result}")


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
