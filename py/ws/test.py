#!/usr/bin/prego

from _test import ClientServerMixin


class HelloWebSocket(ClientServerMixin):
    def test_client_server(self):
        self.make_client_server('./client.py', './server.py', 'config')
