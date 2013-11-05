# -*- mode:python; coding:utf-8 -*-

from hamcrest import contains_string
from prego import TestCase, Task, running


class Hello(TestCase):
    def test_client_server(self):
        servertask = Task('server', detach=True)
        server = servertask.command('./Server.py --Ice.Config=Server.config',
                                    cwd='$testdir', signal=2)
        servertask.assert_that(server.stdout.content, contains_string('Hello World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.command('./Client.py "$(head -1 %s)"' % server.stdout.path,
                           cwd='$testdir')
