#!/usr/bin/prego

import shutil
import tempfile

from hamcrest import contains_string
from prego import TestCase, Task, running, context

# throwaway CA, server and client certificates (see README.md for the
# certificates of the ZeroC demos)
MAKE_CERTS = '''
openssl req -x509 -newkey rsa:2048 -nodes -subj /CN=ca -days 1 \
  -keyout ca.key -out cacert.pem
for name in server client; do
  openssl req -newkey rsa:2048 -nodes -subj /CN=$name -keyout $name.key -out $name.csr
  openssl x509 -req -in $name.csr -CA cacert.pem -CAkey ca.key -CAcreateserial \
    -days 1 -out $name.pem
  openssl pkcs12 -export -in $name.pem -inkey $name.key -passout pass:password \
    -out $name.p12
done
'''


class Secure(TestCase):
    def setUp(self):
        self.certs = tempfile.mkdtemp(prefix='certs-')

    def tearDown(self):
        shutil.rmtree(self.certs, ignore_errors=True)

    def test_client_server(self):
        context.cwd = '$testdir'
        Task('certs').command(MAKE_CERTS, cwd=self.certs, timeout=30)

        servertask = Task('server', detach=True)
        server = servertask.command(
            './server.py --Ice.Config=server.config --IceSSL.DefaultDir=%s' % self.certs,
            signal=2)

        clientside = Task('client')
        clientside.wait_that(server, running())
        clientside.wait_that(server.stdout.content, contains_string('ssl -h'))
        clientside.command(
            './client.py --Ice.Config=client.config --IceSSL.DefaultDir=%s "$(head -1 %s)"' % (
                self.certs, server.stdout.path))

        check = Task('check')
        check.wait_that(server.stdout.content, contains_string('Hello World!'))
        check.wait_that(server.stderr.content,
                        contains_string('SSL summary for incoming connection'))
