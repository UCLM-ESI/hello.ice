#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context


class AMI(TestCase):
    def run_client(self, client):
        clientside = Task(client)
        clientside.wait_that(self.server.stdout.content, contains_string('math1'))
        cmd = clientside.command('./%s "$(head -1 %s)" 4' % (client, self.server.stdout.path))
        clientside.assert_that(cmd.stdout.content, contains_string('24'))

    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        self.server = servertask.command('./Server --Ice.Config=server.config', signal=2)

        self.run_client('Client-end')
        self.run_client('Client-callback')
