#!/usr/bin/prego

from prego import Task, context

from _test import ComposeMixin, ICEGRIDADMIN, wait_until


class IceGridDockerDeploy(ComposeMixin):
    def test_deploy_and_invoke(self):
        context.cwd = '$testdir'
        grid = Task('grid')
        grid.command('make start-grid', timeout=600)
        wait_until(grid, '%s "application describe PrinterApp" >/dev/null 2>&1' % ICEGRIDADMIN)
        for node in 'node1', 'node2':
            wait_until(grid, '%s "node ping %s" >/dev/null 2>&1' % (ICEGRIDADMIN, node))

        deploy = Task('deploy')
        deploy.command('make -C ../py/hello gen-dist', timeout=30)
        deploy.command('make deploy', timeout=180)
        deploy.command('make start-servers', timeout=30)

        client = Task('client')
        client.command('make run-client', timeout=30)
        for server in 'PrinterServer1', 'PrinterServer2':
            wait_until(client, '%s "server show %s stdout" | grep -q "Hello World!"' % (
                ICEGRIDADMIN, server), timeout=10)
