#!/usr/bin/prego

from hamcrest import contains_string
from prego import Task, context

from _test import ComposeMixin, ICEGRIDADMIN, wait_until


class ReplicatedRegistry(ComposeMixin):
    def test_registry_failover(self):
        context.cwd = '$testdir'
        grid = Task('grid')
        grid.command('docker compose up -d --build --remove-orphans', timeout=600)
        wait_until(grid, '%s "registry ping Slave1" >/dev/null 2>&1' % ICEGRIDADMIN)
        wait_until(grid, '%s "node ping node1" >/dev/null 2>&1' % ICEGRIDADMIN)

        client = Task('client')
        client.command('make load-app', timeout=20)
        client.command('make run-client', timeout=30)
        client.assert_that(client.lastcmd.stdout.content, contains_string('HELLO WORLD!'))

        # without the master replica, the slave one resolves the indirect proxy
        failover = Task('failover')
        failover.command('docker compose stop registry1', timeout=30)
        failover.command('make run-client', timeout=90)
        failover.assert_that(failover.lastcmd.stdout.content, contains_string('HELLO WORLD!'))
