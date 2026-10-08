#!/usr/bin/prego

import shutil
import subprocess

from _test import ClientServerMixin


class Hello(ClientServerMixin):
    def test_client_server(self):
        if not shutil.which('ruby') or subprocess.run(
                ['ruby', '-e', 'require "Ice"'], capture_output=True).returncode:
            self.skipTest('Ice for Ruby not installed (see README)')

        self.make_client_server('./client.rb', '../py/hello/server.py',
                                '../py/hello/server.config')
