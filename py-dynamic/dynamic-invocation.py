#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
import Ice

from util import InputStream, OutputStream


class DynamicInvocation(Ice.Application):

    def run(self, args):
        self.args = args
        self.ic = self.communicator()

        if len(args) != 3:
            return self.usage()

        self.create_proxy()
        self.say_things()

    def create_proxy(self):
        self.prx = self.ic.stringToProxy(self.args[1])

    def say_things(self):
        operation = "say"
        mode = Ice.OperationMode.Normal
        out = OutputStream()
        out.writeString(self.args[2])
        inParams = out.finished()

        ok, outParams = self.prx.ice_invoke(operation, mode, inParams)
        if ok:
            result = InputStream(outParams).readBool()
            assert result

        else:
            print "There were an error!"

    def usage(self):
        print "USAGE: {0} <proxy> <message>".format(sys.argv[0])
        return -1


DynamicInvocation().main(sys.argv)

