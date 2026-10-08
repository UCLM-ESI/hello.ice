#!/usr/bin/prego

from hamcrest import contains_string
from prego import Task

from _test import IceGridMixin


class PrinterApp(IceGridMixin):
    def test_invoke(self):
        node1, node2 = self.start_grid('node1', 'node2')

        client = Task('client')
        client.command('make load-app', timeout=10)
        client.command('make run-client', timeout=10)
        client.wait_that(node1.stdout.content, contains_string('0: Hello World!'))

        # "printer1" is a well-known object
        client.command('./well-known.py --Ice.Config=locator.config', timeout=10)
        client.wait_that(node1.stdout.content, contains_string('1: Hello World!'))
