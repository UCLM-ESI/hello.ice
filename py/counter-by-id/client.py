#!/usr/bin/env -S python3 -u

import sys

import Ice
import Example


def main(ic):
    proxy = ic.stringToProxy(sys.argv[1])
    counter = Example.CounterPrx.checkedCast(proxy)

    if counter is None:
        raise RuntimeError('invalid proxy')

    print("get() = '{}'".format(counter.get()))
    print("increment() = '{}'".format(counter.increment()))
    print("increment() = '{}'".format(counter.increment()))
    print("get() = '{}'".format(counter.get()))


if __name__ == '__main__':
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
