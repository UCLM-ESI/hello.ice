#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context


class CounterById(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('./server --Ice.Config=server.config', signal=2)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('counter1'))
        client = clientside.command("./client 'counter1 -t:tcp -h localhost -p 2002'")
        clientside.assert_that(client.stdout.content, contains_string("increment() = '2'"))
