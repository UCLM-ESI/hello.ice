#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, running, context

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar '


class Hello(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('%s Server --Ice.Config=server.config' % java,
                                    signal=2, expected=130)
        servertask.assert_that(server.stdout.content, contains_string('Hello World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.command('%s Client "$(head -1 %s)"' % (java, server.stdout.path))

    def test_client_server_uuid(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('%s ServerUUID --Ice.Config=server.config' % java,
                                    signal=2, expected=130)
        servertask.assert_that(server.stdout.content, contains_string('Hello World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string(' -t -e '))
        clientside.command('%s Client "$(head -1 %s)"' % (java, server.stdout.path))
