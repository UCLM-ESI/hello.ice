#!/usr/bin/prego

import signal

from hamcrest import contains_string
from hamcrest.core.base_matcher import BaseMatcher
from prego import TestCase, Task, context
from prego.net import localhost, listen_port

java = 'java -classpath .:/usr/share/java/ice-3.7.10.jar:/usr/share/java/icestorm-3.7.10.jar'


class ContainsTimes(BaseMatcher):
    def __init__(self, substring, times):
        self.substring = substring
        self.times = times

    def _matches(self, item):
        return item.count(self.substring) == self.times

    def describe_to(self, description):
        description.append_text(
            "a string containing %r %d times" % (self.substring, self.times))


def contains_times(substring, times):
    return ContainsTimes(substring, times)


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
        sub = subscriber.command('%s Subscriber --Ice.Config=subscriber.config' % java,
                                 signal=signal.SIGINT, expected=130)

        publisher = Task('publisher')
        publisher.wait_that(sub.stdout.content, contains_string('Waiting events...'))
        pub = publisher.command('%s Publisher --Ice.Config=publisher.config' % java)
        publisher.assert_that(pub.stdout.content,
                              contains_string("publishing 10 'Hello World' events"))
        publisher.wait_that(sub.stdout.content,
                            contains_times('Event received: Hello World', 10))
