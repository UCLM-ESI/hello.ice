#!/usr/bin/env python3
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys

import Ice

Ice.loadSlice('factorial.ice')
import Example

from work_queue import WorkQueue


class MathI(Example.Math):
    def __init__(self, work_queue):
        self.work_queue = work_queue

    def factorial_async(self, cb, value, current=None):
        self.work_queue.add(cb, value)


class Server(Ice.Application):
    def run(self, argv):
        work_queue = WorkQueue()
        servant = MathI(work_queue)

        broker = self.communicator()

        adapter = broker.createObjectAdapter("MathAdapter")
        math_prx = adapter.add(servant, broker.stringToIdentity("math1"))
        adapter.activate()

        print(math_prx)

        work_queue.start()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        work_queue.destroy()
        return 0


if __name__ == "__main__":
    app = Server()
    sys.exit(app.main(sys.argv))
