#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        container = Services.ContainerPrx.checkedCast(proxy)

        if not container:
            raise RuntimeError('Invalid proxy')

        print container.list()

        return 0

if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
