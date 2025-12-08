#!/usr/bin/env -S python3 -u

import sys
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'upper.ice'))
import Example


class StringUtilI(Example.StringUtil):
    def upper(self, message, current=None):
        print("Client sent:", message)
        return message.upper()


def main(ic):
    servant = StringUtilI()
    adapter = ic.createObjectAdapter("StringAdapter")
    proxy = adapter.add(servant, ic.stringToIdentity("string1"))

    print(proxy)

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("Shutting down server...")
