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
    counter.create("counter2")

    result1 = counter.increment("counter1", 5)
    print(f"After incrementing counter1 by 5: {result1}")

    result2 = counter.increment("counter2", 10)
    print(f"After incrementing counter2 by 10: {result2}")

    value = counter.get("counter1")
    print(f"Value of counter1: {value}")

    all_counters = counter.list()
    print(f"All counters: {all_counters}")


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
