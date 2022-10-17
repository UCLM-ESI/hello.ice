#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

from hamcrest import contains_string
from prego import TestCase, Task, running, context


class ClientServerMixin(TestCase):
    def make_client_server(self, client, server, server_config='Server.config'):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('{} --Ice.Config={}'.format(server, server_config),
                                    signal=2)
        servertask.wait_that(server.stdout.content, contains_string('Hello World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.command('{} "$(head -1 {})"'.format(client, server.stdout.path))
