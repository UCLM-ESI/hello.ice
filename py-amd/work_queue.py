# -*- mode:python; coding:utf-8; tab-width:4 -*-

from threading import Thread
from Queue import Queue


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


class WorkQueue(Thread):
    QUIT = 'QUIT'
    SKIP = 'SKIP'

    def __init__(self):
        super(WorkQueue, self).__init__()
        self.queue = Queue()

    def run(self):
        while True:
            job = self.queue.get()
            if job == self.QUIT:
                self.queue.task_done()
                break

            if job == self.SKIP:
                self.queue.put(self.QUIT)
                Job.execute = Job.cancel
                self.queue.task_done()
                continue

            job.execute()
            self.queue.task_done()

    def add(self, cb, value):
        self.queue.put(Job(cb, value))

    def destroy(self):
        self.queue.put(self.SKIP)
        self.queue.join()


class Job(object):
    def __init__(self, cb, value):
        self.cb = cb
        self.value = value

    def execute(self):
        self.cb.ice_response(factorial(self.value))

    def cancel(self):
        self.cb.ice_exception(Example.RequestCancelException())
