#!/usr/bin/env -S python3 -u

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
        self.prx = Example.HelloPrx.uncheckedCast(self.prx)

    def say_things(self):
        retval = self.prx.say(self.args[2])
        assert retval

    def usage(self):
        print(f"usage: {__file__} <proxy> <message>")
        return -1


if __name__ == "__main__":
    sys.exit(StandardInvocation().main(sys.argv))
