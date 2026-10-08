#!/usr/bin/prego

from hamcrest import contains_string, starts_with
from prego import Task, File

from _test import IceGridMixin, ICEGRIDADMIN

PRINTER2_OUT = '/tmp/printer-py/node2/server-out.txt'


class PrinterApp(IceGridMixin):
    def test_deploy_and_invoke(self):
        setup = Task('setup')
        setup.command('rm -rf /tmp/printer-py')

        self.start_grid('node1', 'node2')

        deploy = Task('deploy')
        deploy.command('make load-app', timeout=10)
        deploy.command('make -C ../hello gen-dist', timeout=30)
        deploy.command('make deploy', timeout=120)
        deploy.command('make start-servers', timeout=20)

        client = Task('client')
        client.command('make run-client', timeout=10)
        client.wait_that(File('/tmp/printer-py/node1/server-out.txt').content,
                         contains_string('Hello World!'))

        client.wait_that(File(PRINTER2_OUT).content,
                         contains_string('@ PrinterServer2.PrinterAdapter'))
        client.command('../hello/client.py --Ice.Config=locator.config "$(head -1 %s)"' %
                       PRINTER2_OUT, timeout=10)
        client.wait_that(File(PRINTER2_OUT).content, contains_string('Hello World!'))

        admin = Task('admin')
        admin.command('%s "server state PrinterServer1"' % ICEGRIDADMIN, timeout=10)
        admin.assert_that(admin.lastcmd.stdout.content, starts_with('active'))
