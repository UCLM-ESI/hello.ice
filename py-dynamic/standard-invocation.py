#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice("example.ice")
import Example


class StandardInvocation(Ice.Application):

    def run(self, args):
        self.args = args
        self.ic = self.communicator()

        if len(args) != 3:
            return self.usage()

        self.create_proxy()
        self.say_things()

    def create_proxy(self):
        self.prx = self.ic.stringToProxy(self.args[1])
        self.prx = Example.PrinterPrx.uncheckedCast(self.prx)

    def say_things(self):
        retval = self.prx.say(self.args[2])
        assert retval

    def usage(self):
        print "USAGE: {0} <proxy> <message>".format(sys.argv[0])
        return -1


StandardInvocation().main(sys.argv)
