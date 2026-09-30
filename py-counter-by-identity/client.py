#!/usr/bin/python3

import sys

import Ice
import Example

with Ice.initialize(sys.argv) as communicator:
    proxy = communicator.stringToProxy(sys.argv[1])
    counter = Example.CounterPrx.checkedCast(proxy)

    if counter is None:
        raise RuntimeError('invalid proxy')

    print("get() = '{}'".format(counter.get()))
    print("increment() = '{}'".format(counter.increment()))
    print("increment() = '{}'".format(counter.increment()))
    print("get() = '{}'".format(counter.get()))
