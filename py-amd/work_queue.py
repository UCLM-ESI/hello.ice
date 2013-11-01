# -*- mode:python; coding:utf-8; tab-width:4 -*-

from threading import Thread


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
