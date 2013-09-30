#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
import Ice

from util import InputStream, OutputStream


class BlobjectI(Ice.Blobject):
    def ice_invoke(self, bytes, current):
        inParams = InputStream(bytes)
        message = inParams.readString()

        print "{0}: {1}".format(current.operation, message)

        out = OutputStream()
        out.writeBool(True)
        outParams = out.finished()

        return True, outParams


class DynamicDispatching(Ice.Application):
    def run(self, args):
        self.broker = self.communicator()

        self.create_adapter()
        self.add_servant()
        self.wait_events()

    def create_adapter(self):
        self.adapter = self.broker.createObjectAdapterWithEndpoints(
            "Adapter", "tcp -h 127.0.0.1 -p 1234")
        self.adapter.activate()

    def add_servant(self):
        servant = BlobjectI()
        oid = self.broker.stringToIdentity("DynamicDispatching")
        proxy = self.adapter.add(servant, oid)
        proxy = proxy.ice_encodingVersion(Ice.Encoding_1_0)

        print "Use proxy: '{0}'".format(proxy)

    def wait_events(self):
        self.shutdownOnInterrupt()
        self.broker.waitForShutdown()


DynamicDispatching().main(sys.argv)
