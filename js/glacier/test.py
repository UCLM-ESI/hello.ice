#!/usr/bin/prego

# The browser side can not be tested here. Instead, a Python client does
# what client.js does: create a Glacier2 session (by WebSocket) and invoke the
# Printer through the router

import shlex

from hamcrest import contains_string
from prego import TestCase, Task, File, exists, context
from prego.net import localhost, listen_port

CLIENT = '''
import sys
import Ice
import Glacier2
Ice.loadSlice('printer.ice')
import Example

with Ice.initialize(sys.argv) as ic:
    router = Glacier2.RouterPrx.checkedCast(ic.getDefaultRouter())
    router.createSession('user', 'password')

    printer = Example.PrinterPrx.uncheckedCast(ic.stringToProxy(sys.argv[-1]))
    printer.write('Hello World!')
'''


class Glacier(TestCase):
    def test_slice2js(self):
        context.cwd = '$testdir'
        build = Task('build')
        build.command('make clean all', timeout=30)
        build.assert_that(File('$testdir/printer.js'), exists())

    def test_invoke_through_router(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command(
            '../../py/hello/server.py --Ice.Config=../../py/hello/server.config', signal=2)

        routertask = Task('glacier2', detach=True)
        routertask.command('glacier2router --Ice.Config=glacier.config', signal=2)

        clientside = Task('client')
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.wait_that(localhost, listen_port(4064))
        clientside.command(
            'python3 -c %s --Ice.Default.Router="Glacier2/router:ws -h 127.0.0.1 -p 4064" '
            '"printer1 -t:tcp -h 127.0.0.1 -p 7070"' % shlex.quote(CLIENT))

        check = Task('check')
        check.wait_that(server.stdout.content, contains_string('Hello World!'))
