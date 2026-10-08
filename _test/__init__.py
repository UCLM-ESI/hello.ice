#!/usr/bin/env -S python3 -u

import inspect
import ipaddress
import json
import os
import shutil
import subprocess
import tempfile

from hamcrest import contains_string, empty, is_not
from prego import TestCase, Task, running, context
from prego.net import localhost, listen_port

ICEGRIDADMIN = 'icegridadmin --Ice.Config=locator.config -u user -p pass -e'


def wait_until(task, condition, timeout=30):
    "Run the shell 'condition' every second until it succeeds"
    return task.command('until {}; do sleep 1; done'.format(condition), timeout=timeout)


class ClientServerMixin(TestCase):
    def make_client_server(self, client, server, server_config='server.config'):
        context.cwd = '$testdir'
        servertask = Task('server', detach=True)
        server = servertask.command('{} --Ice.Config={}'.format(server, server_config),
                                    signal=2)
        servertask.wait_that(server.stdout.content, contains_string('Hello World!'))

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('printer1'))
        clientside.command('{} "$(head -1 {})"'.format(client, server.stdout.path))


class IceGridMixin(TestCase):
    "Runs the IceGrid nodes of the example, with their data in a temporary directory"

    def setUp(self):
        self.icedata = tempfile.mkdtemp(prefix='icedata-')

    def tearDown(self):
        shutil.rmtree(self.icedata, ignore_errors=True)

    def start_grid(self, *nodes):
        context.cwd = '$testdir'

        setup = Task('setup')
        setup.assert_that(localhost, is_not(listen_port(4061)),
                          'another IceGrid registry is running')

        os.makedirs(os.path.join(self.icedata, 'registry'))

        commands = []
        for node in nodes:
            os.makedirs(os.path.join(self.icedata, node))
            task = Task(node, detach=True)
            if commands:
                task.wait_that(localhost, listen_port(4061), timeout=10)

            commands.append(task.command(
                'icegridnode --Ice.Config={0}.config '
                '--IceGrid.Node.Data={1}/{0} '
                '--IceGrid.Registry.LMDB.Path={1}/registry'.format(node, self.icedata),
                signal=2, timeout=None))

        ready = Task('grid ready')
        for node in nodes:
            wait_until(ready, '{} "node ping {}" >/dev/null 2>&1'.format(
                ICEGRIDADMIN, node), timeout=20)

        return commands


def docker(*args, cwd=None):
    return subprocess.run(['docker', *args], cwd=cwd, capture_output=True, text=True).stdout


class ComposeMixin(TestCase):
    "Runs the docker compose services of the example, removing them (and their volumes)"

    def setUp(self):
        if not shutil.which('docker'):
            self.skipTest('docker not installed')

        self.compose('down', '--volumes', '--remove-orphans')

        Task('conflicts').assert_that(
            self.find_conflicts(), empty(),
            'in use by other docker compose projects, run "docker compose down" in them')

    def tearDown(self):
        self.compose('down', '--volumes', '--remove-orphans')

    def compose(self, *args):
        testdir = os.path.dirname(os.path.abspath(inspect.getfile(type(self))))
        return docker('compose', *args, cwd=testdir)

    def find_conflicts(self):
        "Subnets and container names of this example that other examples are using"
        config = json.loads(self.compose('config', '--format', 'json'))
        subnets = [ipaddress.ip_network(ipam['subnet'])
                   for network in config.get('networks', {}).values()
                   for ipam in (network.get('ipam') or {}).get('config', [])]
        names = {service.get('container_name') for service in config['services'].values()}

        conflicts = []
        networks = json.loads(docker('network', 'inspect', *docker('network', 'ls', '-q').split()))
        for network in networks:
            for ipam in network['IPAM']['Config'] or []:
                subnet = ipaddress.ip_network(ipam['Subnet'])
                if any(subnet.overlaps(s) for s in subnets):
                    conflicts.append('subnet {} (network {})'.format(subnet, network['Name']))

        containers = docker('ps', '-a', '--format',
                            '{{.Names}}\t{{.Label "com.docker.compose.project"}}')
        for line in containers.splitlines():
            name, project = line.split('\t')
            if name in names:
                conflicts.append('container {} (project {})'.format(name, project))

        return conflicts
