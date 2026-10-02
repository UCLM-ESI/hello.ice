#!/usr/bin/prego3

import shutil

from hamcrest import contains_string
from prego import TestCase, Task, context

from _test import ClientServerMixin


class Hello(ClientServerMixin):
    def test_client_server(self):
        if not shutil.which('dotnet'):
            self.skipTest('dotnet not installed')

        context.cwd = '$testdir'
        Task('build').command('make', timeout=300)
        self.make_client_server('dotnet bin/client.dll', 'dotnet bin/server.dll')


class HelloDocker(TestCase):
    def test_docker_client_server(self):
        if not shutil.which('docker'):
            self.skipTest('docker not installed')

        context.cwd = '$testdir'
        compose = Task('compose')
        run = compose.command(
            'docker compose up --build --abort-on-container-exit --exit-code-from client;'
            ' rc=$?; docker compose down; exit $rc',
            timeout=900)
        compose.assert_that(run.stdout.content, contains_string('Hello World!'))
