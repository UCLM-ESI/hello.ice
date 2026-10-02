#!/usr/bin/prego

import signal

from hamcrest import contains_string
from prego import TestCase, Task, context

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar'


class AMI(TestCase):
    def run_client(self, client):
        clientside = Task(client)
        clientside.wait_that(self.server.stdout.content, contains_string('math1'))
        cmd = clientside.command('%s %s "$(head -1 %s)" 4' %
                                 (java, client, self.server.stdout.path))
        clientside.assert_that(cmd.stdout.content, contains_string('24'))

    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        self.server = servertask.command('%s Server --Ice.Config=server.config' % java,
                                         signal=signal.SIGINT, expected=130)

        self.run_client('Client_end')
        self.run_client('Client_callback')
