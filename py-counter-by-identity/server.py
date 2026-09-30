#!/usr/bin/python3

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

    for name in ['counter1', 'counter2']:
        print(adapter.add(CounterI(), Ice.stringToIdentity(name)), flush=True)

    adapter.activate()
    communicator.waitForShutdown()
