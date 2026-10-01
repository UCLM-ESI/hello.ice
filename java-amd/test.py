#!/usr/bin/prego

import signal

from hamcrest import contains_string
from prego import TestCase, Task, context

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar'


class AMD(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('%s Server --Ice.Config=server.config' % java,
                                    signal=signal.SIGINT, expected=130)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('math1'))
        client = clientside.command('%s Client "$(head -1 %s)" 4' % (java, server.stdout.path))
        clientside.assert_that(client.stdout.content, contains_string('24'))
