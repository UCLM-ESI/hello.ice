#!/usr/bin/env -S python3 -u

import sys
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'factorial.ice'))
import Example

from work_queue import WorkQueue


class MathI(Example.Math):
    def __init__(self, work_queue):
        self.work_queue = work_queue

    def factorial(self, value, current=None):
        future = Ice.Future()
        self.work_queue.add(future, value)
        return future


def main(ic):
    work_queue = WorkQueue()

    adapter = ic.createObjectAdapter("MathAdapter")
    proxy = adapter.add(MathI(work_queue), Ice.stringToIdentity("math1"))

    print(proxy)

    adapter.activate()
    work_queue.start()

    try:
        ic.waitForShutdown()
    finally:
        work_queue.destroy()

    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("\nShutting down server...")
