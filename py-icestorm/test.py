#!/usr/bin/prego3

from hamcrest import contains_string
from prego import TestCase, Task, context
from prego.net import localhost, listen_port


class IceStorm(TestCase):
    def test_pubsub(self):
        context.cwd = '$testdir'

        setup = Task('setup')
        setup.command('rm -rf db')
        setup.command('mkdir db')

        icebox = Task('icebox', detach=True)
        icebox.command('icebox --Ice.Config=icebox.config', signal=2)

        admin = Task('admin')
        admin.wait_that(localhost, listen_port(10000))
        admin.command('icestormadmin --Ice.Config=icestorm.config -e "destroy PrinterTopic"',
                      expected=None)
        admin.command('icestormadmin --Ice.Config=icestorm.config -e "create PrinterTopic"')

        subscriber = Task('subscriber', detach=True)
        sub = subscriber.command('./subscriber.py --Ice.Config=subscriber.config', signal=2)

        publisher = Task('publisher', detach=True)
        publisher.wait_that(sub.stdout.content, contains_string('Waiting events...'))
        publisher.command('./publisher.py --Ice.Config=publisher.config', signal=2)

        check = Task('check')
        check.wait_that(sub.stdout.content, contains_string('Event received: Hello World #0'))
