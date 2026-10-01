#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, running, context


class Hello(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command(
            'mono --runtime=v4.0 server.exe --Ice.Config=server.config', signal=2)
        servertask.wait_that(server.stdout.content, contains_string('Hello, World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.command('mono --runtime=v4.0 client.exe "$(head -1 %s)"' % server.stdout.path)
