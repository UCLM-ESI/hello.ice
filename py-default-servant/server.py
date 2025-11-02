#!/usr/bin/env -S python3 -u

import sys
import Ice
from uuid import uuid4
from Ice import identityToString as id2str, stringToIdentity as str2id
Ice.loadSlice('printer.ice')
import Example  # noqa


class PrinterI(Example.Printer):
    n = 0

    def write(self, message, current=None):
        print(f"{self.n}: {id2str(current.id)} {message}")
        sys.stdout.flush()
        self.n += 1


def main(ic):
    servant = PrinterI()
    adapter = ic.createObjectAdapter('PrinterAdapter')
    adapter.addDefaultServant(servant, '')

    for _ in range(20):
        print(adapter.createDirectProxy(str2id(f'printer-{uuid4()}')))

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        pass
