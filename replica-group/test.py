#!/usr/bin/prego

from hamcrest import contains_string
from prego import Task, context

from _test import ComposeMixin, ICEGRIDADMIN, wait_until


class ReplicaGroup(ComposeMixin):
    def test_load_balancing(self):
        context.cwd = '$testdir'
        grid = Task('grid')
        grid.command('docker compose up -d --build --remove-orphans', timeout=600)
        for node in 'node1', 'node2':
            wait_until(grid, '%s "node ping %s" >/dev/null 2>&1' % (ICEGRIDADMIN, node))

        # round-robin: consecutive invocations go to different servers
        rr = Task('round-robin')
        rr.command('make round-robin', timeout=20)
        for server in 'ToolServer1', 'ToolServer2':
            wait_until(rr, '%s "server state %s" | grep -q ^active' % (ICEGRIDADMIN, server))

        for i in range(4):
            rr.command('make round-client', timeout=20)
            rr.assert_that(rr.lastcmd.stdout.content, contains_string('HELLO WORLD!'))

        for node in 'node1', 'node2':
            wait_until(rr, 'docker compose logs %s | grep -q "Client sent: Hello World!"' % node,
                       timeout=10)

        for policy in 'random', 'ordered', 'adaptive':
            task = Task(policy)
            task.command('make %s' % policy, timeout=20)
            task.command('make round-client', timeout=20)
            task.assert_that(task.lastcmd.stdout.content, contains_string('HELLO WORLD!'))
