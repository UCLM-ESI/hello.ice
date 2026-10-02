#!/usr/bin/prego3

from hamcrest import contains_string
from prego import TestCase, Task, context


class Upper(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('./server.py --Ice.Config=server.config', signal=2)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('tool1'))
        client = clientside.command('./client.py "$(head -1 %s)"' % server.stdout.path)
        clientside.assert_that(client.stdout.content, contains_string('HELLO WORLD!'))
