#!/usr/bin/env -S python3 -u

import sys
import time
from functools import cached_property

import Ice
from IceGrid import (LocatorPrx, ServerInstanceDescriptor,
                     NodeUpdateDescriptor, ApplicationUpdateDescriptor,
                     NodeObserver)
import IceGrid


Ice.loadSlice('-I. --all PrinterFactory.ice')
import Example


def ensure_proxy(proxy, cls):
    for _ in range(5):
        try:
            proxy.ice_ping()
            break
        except Ice.LocalException:
            time.sleep(0.5)

    retval = cls.checkedCast(proxy)
    if retval is None:
        raise RuntimeError(f'Invalid proxy for {cls.__name__}')

    return retval


class NodeObserverI(NodeObserver):
    def __init__(self, factory):
        self.factory = factory

    def updateServer(self, node, updated_info, current=None):
        print("update server: new state:", node, updated_info.state)

    def nodeInit(self, node, current=None):
        print("node init:", node)

    def nodeDown(self, node_name, current=None):
        print("node down:", node_name)

    def updateAdapter(self, node, adapter, current=None):
        print("update adapter:", node, adapter)


class FactoryI(Example.PrinterFactory):
    def __init__(self, admin_session, app):
        self.admin_session = admin_session
        self.app = app

    def make(self, server_name, current=None):
        node = 'node1'
        server_template = 'PrinterTemplate'

        if node not in self.admin.getAllNodeNames():
            raise Example.FactoryError(
                f"Node '{node}' not defined in app '{self.app}'.")

        if server_template not in self.server_templates:
            raise Example.FactoryError(
                f"Server template '{server_template}' not defined in app '{self.app}'.")

        try:
            self.admin.getServerInfo(server_name)
            state = self.admin.getServerState(server_name)
            if state == IceGrid.ServerState.Inactive:
                self.admin.startServer(server_name)

        except IceGrid.ServerNotExistException:
            self.create_server(node, server_template, server_name)

        proxy = self.get_direct_proxy(server_template, server_name)
        return ensure_proxy(proxy, Example.PrinterPrx)

    @cached_property
    def admin(self):
        return self.admin_session.getAdmin()

    def get_direct_proxy(self, template, server_name):
        adapter_name = self.get_server_template_adapter_name(template)
        adapters = self.admin.getAdapterInfo(f'{server_name}.{adapter_name}')
        if not adapters:
            return None

        dummy_prx = adapters[0].proxy
        return dummy_prx.ice_identity(Ice.stringToIdentity(server_name))

    def get_server_template_adapter_name(self, template):
        template_descriptor = self.server_templates[template]
        adapter_name = template_descriptor.descriptor.adapters[0].name
        return adapter_name

    @cached_property
    def server_templates(self):
        return self.admin.getApplicationInfo(self.app).descriptor.serverTemplates

    def create_server(self, node, template, name):
        server_instance_desc = ServerInstanceDescriptor()
        server_instance_desc.template = template
        server_instance_desc.parameterValues = {'name': name}

        self.admin.instantiateServer(self.app, node, server_instance_desc)
        self.admin.startServer(name)

    def remove_server(self, server_name):
        node_update_desc = NodeUpdateDescriptor()
        node_update_desc.name = self.deploy_node
        node_update_desc.removeServers = [server_name]

        app_update_desc = ApplicationUpdateDescriptor()
        app_update_desc.name = self.app
        app_update_desc.nodes = [node_update_desc]

        self.admin.updateApplication(app_update_desc)


def run(ic):
    admin_session = LocatorPrx.checkedCast(ic.getDefaultLocator()).\
        getLocalRegistry().createAdminSession('user', 'pass')

    servant = FactoryI(admin_session, 'App')

    adapter = ic.createObjectAdapter('PrinterFactory.Adapter')
    adapter.activate()
    proxy = adapter.add(servant, Ice.stringToIdentity('factory'))

    print(proxy)

    ic.waitForShutdown()
    return 0


if __name__ == '__main__':
    with Ice.initialize(sys.argv) as communicator:
        sys.exit(run(communicator))
