#!/usr/bin/env -S python3 -u

import sys
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

    if not math:
        raise RuntimeError('Invalid proxy')

    print(math.factorial(int(sys.argv[2])))

    return 0


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        sys.exit(main(communicator))
