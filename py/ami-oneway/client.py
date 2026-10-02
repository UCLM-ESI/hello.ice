#!/usr/bin/env -S python3 -u

import sys
import time

import Ice
Ice.loadSlice('printer.ice')
import Example


# NOTE: this example uses the deprecated begin_/end_ AMI API (begin_write,
# isSent), kept only for reference. Use the <operation>Async() methods instead,
# which return a future.

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        proxy = proxy.ice_oneway()
        printer = Example.PrinterPrx.uncheckedCast(proxy)

        if not printer:
            raise RuntimeError('Invalid proxy')

        handler = printer.begin_write('Hello World!')

        # polling for sent
        while not handler.isSent():
            time.sleep(0.1)

        return 0


sys.exit(Client().main(sys.argv))
