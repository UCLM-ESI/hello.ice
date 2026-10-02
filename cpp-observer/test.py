#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, Delay, running, context


class Observer(TestCase):
    def test_observer(self):
        context.cwd = '$testdir'

        icebox = Task('icebox', detach=True)
        icebox.command('icebox --Ice.Config=icebox.config', signal=2)

        servertask = Task('server', detach=True)
        server = servertask.command('./server --Ice.Config=server.cfg', signal=2)

        create = Task('create')
        create.wait_that(server.stdout.content, contains_string('factory'))
        creator = create.command('./Create "$(head -1 %s)"' % server.stdout.path)

        monitor = Task('monitor', detach=True)
        monitor.wait_that(creator.stdout.content, contains_string('tcp'))
        mon = monitor.command(
            './Monitor --Ice.Config=monitor.cfg "$(head -1 %s)"' % creator.stdout.path,
            signal=2)

        modify = Task('modify')
        modify.wait_that(mon, running())
        # give Monitor time to subscribe before Modify triggers the notification
        Delay(modify, 0.5)
        cmd = modify.command('./Modify "$(head -1 %s)" true' % creator.stdout.path)
        modify.assert_that(cmd.stdout.content, contains_string('previous value: 0'))
        modify.assert_that(cmd.stdout.content, contains_string('new value: 1'))

        check = Task('check')
        check.wait_that(mon.stdout.content, contains_string('new value: 1'))
