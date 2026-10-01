#!/usr/bin/prego3

from hamcrest import contains_string
from prego import TestCase, Task, context


class Bidir(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('./server.py --Ice.Config=server.config', signal=2)

        clientside = Task('client', detach=True)
        clientside.wait_that(server.stdout.content, contains_string('callback'))
        client = clientside.command('./client.py "$(head -1 %s)"' % server.stdout.path,
                                    signal=2)

        check = Task('check')
        check.wait_that(client.stdout.content, contains_string('1: text 1'))
