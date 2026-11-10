#!/usr/bin/env -S python3 -u

import sys
import Ice
import time

Ice.loadSlice('-I. --all printer.ice PrinterFactory.ice')

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


def main(ic):
    proxy = ic.stringToProxy(sys.argv[1])
    factory = ensure_proxy(proxy, Example.PrinterFactoryPrx)

    proxy1 = factory.make('printer1')
    proxy2 = factory.make('printer2')

    printer = ensure_proxy(proxy1, Example.PrinterPrx)

    printer.write('Hello World!')
    print('ok')

    return 0


with Ice.initialize(sys.argv) as communicator:
    sys.exit(main(communicator))
