#!/usr/bin/env -S python3 -u

import sys
import logging
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'counter.ice'))
import Example

logger = logging.getLogger('CounterServer')
logging.basicConfig(level=logging.INFO)


class CounterI(Example.Counter):
    def __init__(self):
        self.counters = {}

    def create(self, name, current=None):
        logger.info(f"Received request to create counter: {name}")
        if name not in self.counters:
            self.counters[name] = 0
        else:
            logger.info(f"Counter {name} already exists")

    def increment(self, name, delta, current=None):
        logger.info(f"Received request to increment {name} by {delta}")
        if name not in self.counters:
            raise Example.NotFound(name)

        self.counters[name] += delta
        return self.counters[name]

    def get(self, name, current=None):
        logger.info(f"Received request to get counter: {name}")
        if name not in self.counters:
            raise Example.NotFound(name)

        return self.counters[name]

    def list(self, current=None):
        logger.info("Received request to list counters")
        return self.counters.copy()


def main(ic):
    servant = CounterI()
    adapter = ic.createObjectAdapter("CounterAdapter")
    proxy = adapter.add(servant, ic.stringToIdentity("counter-server"))

    print(proxy)

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("\nShutting down server...")
