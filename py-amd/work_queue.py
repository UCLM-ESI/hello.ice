from threading import Thread
from queue import Queue
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

    def add(self, future, value):
        self.queue.put(Job(future, value))

    def destroy(self):
        self.queue.put(self.QUIT)
        self.queue.join()


class Job:
    def __init__(self, future, value):
        self.future = future
        self.value = value

    def execute(self):
        self.future.set_result(factorial(self.value))

    def cancel(self):
        self.future.set_exception(Example.RequestCancelException())
