#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar'


class CounterByKey(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('%s Server --Ice.Config=server.config' % java,
                                    signal=2, expected=130)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('counter'))
        client = clientside.command('%s Client "$(head -1 %s)"' % (java, server.stdout.path))
        clientside.assert_that(client.stdout.content,
                               contains_string('After incrementing counter1 by 5: 5'))
