#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import threading
import time
from functools import lru_cache

import Ice
from IceGrid import (LocatorPrx, ServerInstanceDescriptor,
                     NodeUpdateDescriptor, ApplicationUpdateDescriptor,
                     NodeObserverPrx, NodeObserver, ServerState)
import IceGrid

Ice.loadSlice('-I. --all factory.ice')
import IceCloud  # noqa


class NodeObserverI(NodeObserver):
    def __init__(self, factory):
        self.factory = factory

    def updateServer(self, node, updated_info, current):
        print("updateServer: new state: {}".format(updated_info.state))
        return
        if updated_info.state in [ServerState.Inactive, ServerState.Destroyed]:
            self.factory.remove_server(updated_info.id)

    def nodeDown(self, node_name, current):
        print("node {} down".format(node_name))
        sys.stdout.flush()

    def nodeInit(self, node, current):
        print("nodeInit called", node)

    def updateAdapter(self, node, adapter, current):
        print("updateAdapter called", node, adapter)


class KeepAliveThread(threading.Thread):
    def __init__(self, admin_session):
        super().__init__(daemon=True)
        self.session = admin_session

    def run(self):
        while True:
            print('keep alive')
            self.session.keepAlive()
            time.sleep(5)


class FactoryI(IceCloud.ServerFactory):
    def __init__(self, admin_session, app):
        self.admin_session = admin_session
        self.app = app

    def make(self, node, server_template, params, current):
        if node not in self.admin.getAllNodeNames():
            raise IceCloud.CreationError("Node '{}' is not defined in application '{}'.".format(node, self.app))

        if server_template not in self.server_templates:
            raise IceCloud.CreationError("Server template '{}' is not defined in application '{}'.".format(server_template, self.app))

        if 'name' not in params:
            raise IceCloud.CreationError("Parameter 'name' is mandatory.")

        try:
            server_name = params['name']
            self.admin.getServerInfo(server_name)
            state = self.admin.getServerState(server_name)
            if state == IceGrid.ServerState.Inactive:
                self.admin.startServer(server_name)

        except IceGrid.ServerNotExistException:
            self.create_server(node, server_template, params)

        proxy = self.get_direct_proxy(server_template, server_name)
        proxy.ice_ping()
        return proxy

    @property
    @lru_cache(None)
    def admin(self):
        return self.admin_session.getAdmin()

    @property
    @lru_cache(None)
    def server_templates(self):
        return self.admin.getApplicationInfo(self.app).descriptor.serverTemplates

    def get_server_template_adapter_name(self, template):
        template_descriptor = self.server_templates[template]
        adapter_name = template_descriptor.descriptor.adapters[0].name
        return adapter_name

    def get_direct_proxy(self, template, server_name):
        adapter_name = self.get_server_template_adapter_name(template)
        adapters = self.admin.getAdapterInfo('{}.{}'.format(server_name, adapter_name))
        if not adapters:
            return None

        dummy_prx = adapters[0].proxy
        return dummy_prx.ice_identity(Ice.stringToIdentity(server_name))

    def create_server(self, node, template, params):
        server_instance_desc = ServerInstanceDescriptor()
        server_instance_desc.template = template
        server_instance_desc.parameterValues = params

        self.admin.instantiateServer(self.app, node, server_instance_desc)
        self.admin.startServer(params['name'])

    def remove_server(self, server_name):
        print('Trying to remove server {}'.format(server_name))
        node_update_desc = NodeUpdateDescriptor()
        node_update_desc.name = self.deploy_node
        node_update_desc.removeServers = [server_name]

        app_update_desc = ApplicationUpdateDescriptor()
        app_update_desc.name = self.app
        app_update_desc.nodes = [node_update_desc]

        self.admin.updateApplication(app_update_desc)


class FactoryServer(Ice.Application):
    def run(self, argv):
        self.broker = self.communicator()
        self.adapter = self.broker.createObjectAdapter('Adapter')
        self.adapter.activate()

        self.properties = self.broker.getProperties()

        self.servant = FactoryI(
            self.admin_session,
            self.get_application())

        print(self. adapter.add(self.servant, self.get_factory_identity()))

        self.set_node_observer()
        self.keep_session()

        self.shutdownOnInterrupt()
        self.broker.waitForShutdown()

        return 0

    @property
    @lru_cache(None)
    def admin_session(self):
        user = self.properties.getProperty('user')
        pwd = self.properties.getProperty('pwd')

        registry = LocatorPrx.checkedCast(self.communicator().getDefaultLocator()).getLocalRegistry()
        return registry.createAdminSession(user, pwd)

    def get_application(self):
        application = self.properties.getProperty('app')
        if not application:
            sys.tracebacklimit = 0
            raise ValueError(
                "You must provide the 'app' configuration property.")#

        return application

    def get_factory_identity(self):
        return self.broker.stringToIdentity(
            self.properties.getPropertyWithDefault('Identity', 'factory'))

    def set_node_observer(self):
        observer = NodeObserverI(self.servant)
        observer = NodeObserverPrx.uncheckedCast(self.adapter.addWithUUID(observer))
        self.admin_session.setObservers(None, observer, None, None, None)

    def keep_session(self):
        keep_alive_thread = KeepAliveThread(self.admin_session)
        keep_alive_thread.start()


if __name__ == '__main__':
    sys.exit(FactoryServer().main(sys.argv))
