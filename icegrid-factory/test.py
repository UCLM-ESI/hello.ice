#!/usr/bin/prego

from hamcrest import contains_string
from prego import Task, File, context

from _test import IceGridMixin, ICEGRIDADMIN


class Factory(IceGridMixin):
    def test_factory(self):
        context.cwd = '$testdir'
        setup = Task('setup')
        setup.command('rm -f *.out *.err')

        self.start_grid('node1')

        client = Task('client')
        client.command('%s "application add app.xml"' % ICEGRIDADMIN, timeout=10)
        client.command('make run-client', timeout=30)
        client.assert_that(client.lastcmd.stdout.content, contains_string('ok'))
        client.wait_that(File('$testdir/printer.out').content, contains_string('Hello World!'))

        # "printer2" was instantiated by the factory from the server template
        client.command('%s "server list"' % ICEGRIDADMIN, timeout=10)
        client.assert_that(client.lastcmd.stdout.content, contains_string('printer2'))
