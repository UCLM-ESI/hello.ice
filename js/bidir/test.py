#!/usr/bin/prego

# The browser side can not be tested here. Instead, the Python client of
# ../../py/bidir plays its role, using the same proxy (by WebSocket)

from hamcrest import contains_string
from prego import TestCase, Task, File, exists, context

PROXY = 'callback:ws -h 127.0.0.1 -p 7071'


class Bidir(TestCase):
    def test_slice2js(self):
        context.cwd = '$testdir'
        build = Task('build')
        build.command('make clean all', timeout=30)
        build.assert_that(File('$testdir/printer.js'), exists())
        build.assert_that(File('$testdir/callback.js'), exists())

    def test_bidir_server_by_websocket(self):
        context.cwd = '$testdir/../../py/bidir'
        servertask = Task('server', detach=True)
        server = servertask.command('./server.py --Ice.Config=server-ws.config', signal=2)

        clientside = Task('client', detach=True)
        clientside.wait_that(server.stdout.content, contains_string(':ws '))
        client = clientside.command("./client.py '%s'" % PROXY, signal=2)

        check = Task('check')
        check.wait_that(client.stdout.content, contains_string('1: text 1'))
