#!/usr/bin/prego

from hamcrest import contains_string
from prego import TestCase, Task, context

TEXT = 'Hello Dynamic World!'


class Dynamic(TestCase):
    def say(self, server, client, identity):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        srv = servertask.command('./%s.py' % server, signal=2)

        clientside = Task('client')
        clientside.wait_that(srv.stdout.content, contains_string('Use proxy'))
        clientside.command("./%s.py '%s -t:tcp -h 127.0.0.1 -p 1234' '%s'" % (
            client, identity, TEXT))
        clientside.wait_that(srv.stdout.content, contains_string('say: ' + TEXT))

    def test_dynamic_invocation(self):
        self.say('standard-dispatching', 'dynamic-invocation', 'StandardDispatching')

    def test_dynamic_dispatching(self):
        self.say('dynamic-dispatching', 'standard-invocation', 'DynamicDispatching')

    def test_dynamic_invocation_and_dispatching(self):
        self.say('dynamic-dispatching', 'dynamic-invocation', 'DynamicDispatching')
