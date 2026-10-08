#!/usr/bin/prego

from prego import Task, context

from _test import ClientServerMixin


class HelloWebSocket(ClientServerMixin):
    def test_client_server(self):
        context.cwd = '$testdir'
        Task('build').command('make clean all', timeout=120)
        self.make_client_server('./client', './server', 'config')
