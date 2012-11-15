#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
from threading import Thread
from Queue import Queue

import Ice
Ice.loadSlice('factorial.ice')
import Example


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


class Worker(Thread):
    QUIT = 'QUIT'

    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            job = self.queue.get()
            if job == Worker.QUIT:
                self.queue.task_done()
                break

            job.execute()
            self.queue.task_done()


class Job(object):
    def __init__(self, cb, value):
        self.cb = cb
        self.value = value

    def execute(self):
        self.cb.ice_response(factorial(self.value))


class MathI(Example.Math):
    def __init__(self, queue):
        self.queue = queue

    def factorial_async(self, cb, value, current=None):
        self.queue.put(Job(cb, value))


class Server(Ice.Application):
    def run(self, argv):
        queue = Queue()
        worker = Worker(queue)

        broker = self.communicator()

        adapter = broker.createObjectAdapter("MathAdapter")
        print adapter.add(MathI(queue), broker.stringToIdentity("math1"))
        adapter.activate()

        worker.start()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        queue.put(Worker.QUIT)
        queue.join()
        return 0


sys.exit(Server().main(sys.argv))
