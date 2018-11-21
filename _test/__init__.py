#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from unittest import TestCase
from prego import Task, running
from hamcrest import contains_string


class ClientServerMixin(TestCase):
    def make_client_server(self, client, server):
        servertask = Task('server', detach=True)
        server = servertask.command('{} --Ice.Config=Server.config'.format(server),
                                    cwd='$testdir', signal=2)
        servertask.assert_that(server.stdout.content, contains_string('Hello World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.command('{} "$(head -1 {})"'.format(client, server.stdout.path),
                           cwd='$testdir')
