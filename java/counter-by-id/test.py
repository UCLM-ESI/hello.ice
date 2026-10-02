#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar'


class CounterById(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('%s Server --Ice.Config=server.config' % java,
                                    signal=2, expected=130)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('counter1'))
        client = clientside.command("%s Client 'counter1 -t:tcp -h localhost -p 2002'" % java)
        clientside.assert_that(client.stdout.content, contains_string("increment() = '2'"))
