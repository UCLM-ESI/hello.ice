#!/usr/bin/python -u
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys
from Queue import Queue

import Ice
Ice.loadSlice('factorial.ice')
import Example

from work_queue import Worker, Job


class MathI(Example.Math):
    def __init__(self, queue):
        self.queue = queue

    def factorial_async(self, cb, value, current=None):
        self.queue.put(Job(cb, value))


class Server(Ice.Application):
    def run(self, argv):
        queue = Queue()
        worker = Worker(queue)
        servant = MathI(queue)

        broker = self.communicator()

        adapter = broker.createObjectAdapter("MathAdapter")
        print adapter.add(servant, broker.stringToIdentity("math1"))
        adapter.activate()

        worker.start()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        queue.put(Worker.QUIT)
        queue.join()
        return 0


sys.exit(Server().main(sys.argv))
