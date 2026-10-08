#!/usr/bin/prego

from hamcrest import contains_string
from prego import Task, context

from _test import ComposeMixin, ICEGRIDADMIN, wait_until


class StatefulReplicationRedisCluster(ComposeMixin):
    def test_shared_state(self):
        context.cwd = '$testdir'
        grid = Task('grid')
        grid.command('docker compose up -d --build --remove-orphans', timeout=600)
        wait_until(grid, 'make -s cluster-status | grep -c master | grep -q 3')
        for node in 'node1', 'node2':
            wait_until(grid, '%s "node ping %s" >/dev/null 2>&1' % (ICEGRIDADMIN, node))

        # the round-robin group sends each invocation to a different server, but
        # both share the counter stored in the Redis cluster
        client = Task('client')
        client.command('make load-app', timeout=20)
        client.command('make run-client', timeout=60)
        client.assert_that(client.lastcmd.stdout.content,
                           contains_string('After incrementing counter1 by 5: 5'))
        client.command('make run-client', timeout=60)
        client.assert_that(client.lastcmd.stdout.content,
                           contains_string('After incrementing counter1 by 5: 10'))

        for node in 'node1', 'node2':
            wait_until(client, 'docker compose logs %s | grep -q "increment counter1"' % node,
                       timeout=10)
