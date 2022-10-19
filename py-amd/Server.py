#!/usr/bin/env -S python3 -u
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys

import Ice
Ice.loadSlice('factorial.ice')
import Example

from work_queue import WorkQueue


class MathI(Example.Math):
    def __init__(self, work_queue):
        self.work_queue = work_queue

    def factorial(self, value, current=None):
        future = Ice.Future()
        self.work_queue.add(future, value)
        return future


class Server(Ice.Application):
    def run(self, argv):
        work_queue = WorkQueue()
        servant = MathI(work_queue)

        broker = self.communicator()

        adapter = broker.createObjectAdapter("MathAdapter")
        print(adapter.add(servant, broker.stringToIdentity("math1")))
        adapter.activate()

        work_queue.start()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        work_queue.destroy()
        return 0

sys.exit(Server().main(sys.argv))
