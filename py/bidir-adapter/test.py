#!/usr/bin/prego

import shlex

from hamcrest import contains_string
from prego import TestCase, Task, context

# What ../../js/hello does in the browser: register a Printer in the
# BidirAdapter (by WebSocket) and receive the invocations through that connection
PEER = '''
import sys
import Ice
Ice.loadSlice('-I{} BidirAdapter.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('../hello/printer.ice')
import Utils
import Example


class PrinterI(Example.Printer):
    def write(self, message, current):
        print('message received:', message, flush=True)


with Ice.initialize(sys.argv) as ic:
    local_adapter = ic.createObjectAdapter('')
    remote_adapter = Utils.BidirAdapterPrx.checkedCast(
        ic.stringToProxy('bidir-adapter -t:ws -h 127.0.0.1 -p 7071'))
    remote_adapter.ice_getConnection().setAdapter(local_adapter)

    print(remote_adapter.add(local_adapter.addWithUUID(PrinterI())), flush=True)
    try:
        ic.waitForShutdown()
    except KeyboardInterrupt:
        pass
'''


class BidirAdapter(TestCase):
    def test_invoke_bidir_peer(self):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('./server.py --Ice.Config=server-ws.config', signal=2)

        peertask = Task('peer', detach=True)
        peertask.wait_that(server.stdout.content, contains_string('bidir-adapter'))
        peer = peertask.command('python3 -c %s' % shlex.quote(PEER), signal=2)

        clientside = Task('client')
        clientside.wait_that(peer.stdout.content, contains_string(' -t -e 1.1'))
        clientside.command('../hello/client.py "$(head -1 %s)"' % peer.stdout.path)

        check = Task('check')
        check.wait_that(peer.stdout.content, contains_string('message received: Hello World!'))
        check.wait_that(server.stdout.content, contains_string('forward to'))
