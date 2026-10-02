#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context


class AMD(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('./server --Ice.Config=server.config', signal=2)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('math1'))
        client = clientside.command('./client "$(head -1 %s)" 4' % server.stdout.path)
        clientside.assert_that(client.stdout.content, contains_string('24'))
