#!/usr/bin/prego

from prego import Task, context

from _test import ComposeMixin, ICEGRIDADMIN, wait_until


class IceGridDocker(ComposeMixin):
    def test_invoke(self):
        context.cwd = '$testdir'
        grid = Task('grid')
        grid.command('docker compose up -d --build --remove-orphans', timeout=600)
        wait_until(grid, '%s "application describe PrinterApp" >/dev/null 2>&1' % ICEGRIDADMIN)

        client = Task('client')
        client.command('make run-client', timeout=30)
        client.command('make run-client-wko', timeout=30)
        wait_until(client, '[ $(docker compose logs node1 | grep -c "Hello World!") -eq 2 ]',
                   timeout=10)
