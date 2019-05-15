#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import threading
import time

import Ice
from IceGrid import (LocatorPrx, ServerInstanceDescriptor,
                     NodeUpdateDescriptor, ApplicationUpdateDescriptor,
                     NodeObserverPrx, NodeObserver, ServerState)
import IceGrid

Ice.loadSlice('-I. --all factory.ice')
import Example  # noqa


class NodeObserverI(NodeObserver):
    def __init__(self, factory):
        self.factory = factory

    def updateServer(self, node, updated_info, current):
        print("updateServer: new state: {}".format(updated_info.state))
        return
        if updated_info.state in [ServerState.Inactive, ServerState.Destroyed]:
            self.factory.remove_server(updated_info.id)

    def nodeDown(self, node_name, current):
        print("Node {} down".format(node_name))
        sys.stdout.flush()

    def nodeInit(self, node,  current):
        print("nodeInit called", node)

    def updateAdapter(self, node, adapter, current):
        print("updateAdapter called", node, adapter)


class KeepAliveThread(threading.Thread):
    def __init__(self, admin_session):
        super().__init__(daemon=True)
        self.session = admin_session

    def run(self):
        while True:
            print('Keep alive')
            self.session.keepAlive()
            time.sleep(5)


class FactoryI(Example.PrinterFactory):
    def __init__(self, admin_session):
        self.admin_session = admin_session
        self._admin = None

        self.app = 'App'
        self.deploy_node = 'node1'
        self.template = 'PrinterServer'
        self.template_adapter = 'PrinterAdapter'

    def make(self, server_name, current):
        try:
            self.admin().getServerInfo(server_name)
            state = self.admin().getServerState(server_name)
            if state == IceGrid.ServerState.Inactive:
                self.admin().startServer(server_name)

        except IceGrid.ServerNotExistException:
            self.create_server(server_name)

        retval = self.get_direct_proxy(server_name, broker=current.adapter.getCommunicator())
        return Example.PrinterPrx.checkedCast(retval)

    def admin(self):
        if self._admin is not None:
            return self._admin

        self._admin = self.admin_session.getAdmin()
        return self._admin

    def get_direct_proxy(self, server_name, broker):
        adapters = self.admin().getAdapterInfo('{}.{}'.format(server_name, self.template_adapter))
        if not adapters:
            return None

        dummy_prx = adapters[0].proxy
        return dummy_prx.ice_identity(broker.stringToIdentity(server_name))

    def create_server(self, server_name):
        server_instance_desc = ServerInstanceDescriptor()
        server_instance_desc.template = self.template
        server_instance_desc.parameterValues = {
            'name': server_name,
        }

        self.admin().instantiateServer(self.app, self.deploy_node, server_instance_desc)
        self.admin().startServer(server_name)

    def remove_server(self, server_name):
        print('Trying to remove server {}'.format(server_name))
        node_update_desc = NodeUpdateDescriptor()
        node_update_desc.name = self.deploy_node
        node_update_desc.removeServers = [server_name]

        app_update_desc = ApplicationUpdateDescriptor()
        app_update_desc.name = self.app
        app_update_desc.nodes = [node_update_desc]

        self.admin().updateApplication(app_update_desc)


class FactoryServer(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        self.adapter = broker.createObjectAdapter('Adapter')
        self.adapter.activate()

        self.properties = broker.getProperties()
        self.admin_session = self.get_admin_session()

        identity = broker.stringToIdentity(
            self.properties.getPropertyWithDefault('Identity', 'factory'))

        self.servant = FactoryI(self.admin_session)
        proxy = self. adapter.add(self.servant, identity)
        print(proxy)

        self.set_node_observer()
        self.keep_session()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

    def get_admin_session(self):
        user = self.properties.getProperty('user')
        pwd = self.properties.getProperty('pwd')

        registry = LocatorPrx.checkedCast(self.communicator().getDefaultLocator()).getLocalRegistry()
        return registry.createAdminSession(user, pwd)

    def set_node_observer(self):
        observer = NodeObserverI(self.servant)
        observer = NodeObserverPrx.uncheckedCast(self.adapter.addWithUUID(observer))
        print(observer)
        self.admin_session.setObservers(None, observer, None, None, None)

    def keep_session(self):
        keep_alive_thread = KeepAliveThread(self.admin_session)
        keep_alive_thread.start()


if __name__ == '__main__':
    sys.exit(FactoryServer().main(sys.argv))
