#!/usr/bin/env -S python3 -u

import sys
import Ice

Ice.loadSlice("example.ice")
import Example


class PrinterI(Example.Hello):

    def say(self, message, current=None):
        print("say:", message)
        return True


class StandardDispatching(Ice.Application):

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
        srv = PrinterI()
        oid = self.ic.stringToIdentity("StandardDispatching")
        prx = self.oa.add(srv, oid)

        print("Use proxy: '{0}'".format(prx))

    def wait_events(self):
        self.shutdownOnInterrupt()
        self.ic.waitForShutdown()


if __name__ == "__main__":
    sys.exit(StandardDispatching().main(sys.argv))
