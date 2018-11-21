#!/usr/bin/prego
# -*- mode:python; coding:utf-8 -*-

from _test import ClientServerMixin


class Hello(ClientServerMixin):
    def test_client_server(self):
        self.make_client_server('./Client', './Server')
