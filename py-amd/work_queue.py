# -*- mode:python; coding:utf-8; tab-width:4 -*-

from threading import Thread
from Queue import Queue
import Example


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


class WorkQueue(Thread):
    QUIT = 'QUIT'
    CANCEL = 'CANCEL'

    def __init__(self):
        super(WorkQueue, self).__init__()
        self.queue = Queue()

    def run(self):
        for job in iter(self.queue.get, self.QUIT):
            job.execute()
            self.queue.task_done()

        self.queue.task_done()
        self.queue.put(self.CANCEL)

        for job in iter(self.queue.get, self.CANCEL):
            job.cancel()
            self.queue.task_done()

        self.queue.task_done()

    def add(self, cb, value):
        self.queue.put(Job(cb, value))

    def destroy(self):
        self.queue.put(self.QUIT)
        self.queue.join()


class Job(object):
    def __init__(self, cb, value):
        self.cb = cb
        self.value = value

    def execute(self):
        self.cb.ice_response(factorial(self.value))

    def cancel(self):
        self.cb.ice_exception(Example.RequestCancelException())
