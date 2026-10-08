#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar '


class Bidir(TestCase):
    def test_client_server(self):
        context.cwd = '$testdir'
        Task('build').command('make clean all', timeout=120)

        servertask = Task('server', detach=True)
        server = servertask.command('%s Server --Ice.Config=server.config' % java,
                                    signal=2, expected=130)

        clientside = Task('client', detach=True)
        clientside.wait_that(server.stdout.content, contains_string('callback'))
        client = clientside.command('%s Client "$(head -1 %s)"' % (java, server.stdout.path),
                                    signal=2, expected=130)

        check = Task('check')
        check.wait_that(client.stdout.content, contains_string('1: text 1'))
        check.wait_that(server.stdout.content, contains_string('new printer'))
