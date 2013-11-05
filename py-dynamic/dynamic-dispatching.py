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
        self.ic = self.communicator()

        self.create_adapter()
        self.append_servant()
        self.wait_events()

    def create_adapter(self):
        self.oa = self.ic.createObjectAdapterWithEndpoints(
            "Adapter", "tcp -h 127.0.0.1 -p 1234")
        self.oa.activate()

    def append_servant(self):
        srv = BlobjectI()
        oid = self.ic.stringToIdentity("DynamicDispatching")
        prx = self.oa.add(srv, oid)

        print "Use proxy: '{0}'".format(prx)

    def wait_events(self):
        self.shutdownOnInterrupt()
        self.ic.waitForShutdown()


DynamicDispatching().main(sys.argv)

