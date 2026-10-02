#!/usr/bin/env -S python3 -u

import sys
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'counter.ice'))
import Example


def main(ic):
    proxy = ic.stringToProxy(sys.argv[1])
    counter = Example.CounterPrx.checkedCast(proxy)

    if not counter:
        raise RuntimeError('Invalid proxy')

    counter.create("counter1")
    counter.increment("counter1", 5)
    print(f"After incrementing counter1 by 5: {counter.get("counter1")}")


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
