#!/usr/bin/env python3

import sys

import Ice
import Example


class CounterI(Example.Counter):
    def __init__(self):
        self.value = 0

    def increment(self, current):
        self.value += 1
        return self.value

    def get(self, current):
        return self.value


with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapter('CounterAdapter')

    proxy1 = adapter.add(CounterI(), Ice.stringToIdentity('counter1'))
    proxy2 = adapter.add(CounterI(), Ice.stringToIdentity('counter2'))

    print(proxy1)
    print(proxy2)

    adapter.activate()
    communicator.waitForShutdown()
