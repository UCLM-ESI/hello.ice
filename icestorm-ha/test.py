#!/usr/bin/prego

from hamcrest import contains_string
from prego import Task, context

from _test import ComposeMixin, ICEGRIDADMIN, wait_until

EVENTS = 'docker compose logs node2 | grep -c "Event received"'


class IceStormHA(ComposeMixin):
    def test_events_survive_replica_failure(self):
        context.cwd = '$testdir'
        grid = Task('grid')
        grid.command('docker compose up -d --build --remove-orphans', timeout=600)
        for node in 'node1', 'node2', 'node3':
            wait_until(grid, '%s "node ping %s" >/dev/null 2>&1' % (ICEGRIDADMIN, node))
        grid.command('make load-app', timeout=20)

        # EventServer1 (node1) publishes, EventServer2 (node2) subscribes
        events = Task('events')
        wait_until(events, '[ $(%s) -gt 0 ]' % EVENTS, timeout=60)

        subscribertask = Task('subscriber', detach=True)
        subscriber = subscribertask.command('make -s run-subscriber', signal=2,
                                            timeout=None, expected=None)

        check = Task('check')
        check.wait_that(subscriber.stdout.content, contains_string('Event received'),
                        timeout=20)

        # one of the three IceStorm replicas fails, the events keep arriving
        failover = Task('failover')
        failover.command('docker compose stop node3', timeout=30)
        failover.command('n=$(%s); until [ $(%s) -ge $((n + 5)) ]; do sleep 1; done' % (
            EVENTS, EVENTS), timeout=30)
