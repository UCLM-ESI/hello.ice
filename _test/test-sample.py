#!/usr/bin/prego

import glob
from hamcrest import is_not, contains_string
from prego import TestCase, Task, context, terminated
from prego.net import localhost, listen_port


# def wait_clients(clients):
#     task = Task('wait clients end')
#     for client in clients:
#         task.wait_that(client, terminated(), timeout=60)


# class HelpTests(TestCase):
#     def test_help(self):
#         for fname in glob.glob('*.py'):
#             if 'stress' in fname or 'client' in fname:
#                 continue

#             app = Task()
#             app.command('./{}'.format(fname), expected=1)
#             app.assert_that(app.lastcmd.stdout.content,
#                         contains_string('Usage: ./{} <port>'.format(fname)))


class FactoryTests(TestCase):
    def test_make_printer(self):
        client = Task()
        client.command('./client.py --Ice.Config=locator.config factory', cwd='icegrid-factory')



# class UDPTests(TestCase):
#     def setUp(self):
#         context.port = 2000

#     def run_server(self, prog):
#         server = Task(detach=True)
#         server.assert_that(localhost,
#                            is_not(listen_port(context.port, proto='udp')))
#         server.command('./{0} $port'.format(prog), timeout=15, expected=None)

#         clients = self.run_clients()
#         wait_clients(clients)

#     def run_clients(self):
#         Task().wait_that(localhost, listen_port(context.port, proto='udp'))

#         clients = []
#         for i in range(10):
#             req = 'hello-%s' % i
#             client = Task(detach=True)
#             client.command('echo %s | ./UDP_client.py localhost $port' % req,
#                            timeout=15)
#             client.assert_that(client.lastcmd.stdout.content,
#                                contains_string("Reply is '" + req.upper()))

#             clients.append(client)

#         return clients

#     def test_basic(self):
#         self.run_server('UDP_server.py')

#     def test_fork(self):
#         self.run_server('UDP_fork.py')

#     def test_SocketServer(self):
#         self.run_server('UDP_SS.py')

#     def test_SocketServer_fork(self):
#         self.run_server('UDP_SS_fork.py')


# class TCPTests(TestCase):
#     def setUp(self):
#         context.port = 2000
#         context.timeout = 20

#     def run_server(self, prog):
#         server = Task('server', detach=True)
#         server.assert_that(localhost,
#                            is_not(listen_port(context.port, proto='tcp')))
#         server.command("./{0} $port".format(prog), expected=None)

#         clients = self.run_clients()
#         wait_clients(clients)

#     def run_clients(self):
#         Task().wait_that(localhost, listen_port(context.port, proto='tcp'))

#         clients = []
#         for i in range(10):
#             req = 'hello-%s' % i
#             client = Task('client', detach=True)
#             client.command('echo %s | ./TCP_client.py localhost $port' % req)
#             client.assert_that(client.lastcmd.stdout.content,
#                                contains_string("Reply is '" + req.upper()))
#             clients.append(client)

#         return clients

#     def test_basic(self):
#         self.run_server('TCP_server.py')

#     def test_SocketServer(self):
#         self.run_server('TCP_SS.py')

#     def test_fork(self):
#         self.run_server('TCP_fork.py')

#     def test_SocketServer_fork(self):
#         self.run_server('TCP_SS_fork.py')

#     def test_process(self):
#         self.run_server('TCP_process.py')

#     def test_workers(self):
#         self.run_server('TCP_workers.py')

#     def test_thread(self):
#         self.run_server('TCP_thread.py')

#     def test_SocketServer_thread(self):
#         self.run_server('TCP_SS_thread.py')

#     def test_select(self):
#         self.run_server('TCP_select.py')

#     def test_asyncore(self):
#         self.run_server('TCP_asyncore.py')

#     def test_twisted(self):
#         self.run_server('TCP_twisted.py')


# class TCP6Tests(TestCase):
#     def setUp(self):
#         context.port = 2000
#         context.timeout = 40

#     def run_server(self, prog):
#         server = Task('server', detach=True)
#         server.assert_that(localhost,
#                            is_not(listen_port(context.port, proto='tcp')))
#         server.command("./{0} $port".format(prog), expected=None)

#     def run_clients(self, prog):
#         Task().wait_that(localhost, listen_port(context.port, proto='tcp'))

#         clients = []
#         for i in range(10):
#             req = 'hello-%s' % i
#             client = Task('client', detach=True)
#             client.command('echo {0} | ./{1} $port'.format(req, prog))
#             client.assert_that(client.lastcmd.stdout.content,
#                                contains_string("Reply is '" + req.upper()))
#             clients.append(client)

#         return clients

#     def test_basic_with_ipv4_client(self):
#         self.run_server('TCP6_server.py')
#         clients = self.run_clients('TCP_client.py 127.0.0.1')
#         wait_clients(clients)

#     def test_basic_with_ipv6_client(self):
#         self.run_server('TCP6_server.py')
#         clients = self.run_clients('TCP6_client.py ::1')
#         wait_clients(clients)
