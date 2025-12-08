#!/usr/bin/env -S python3 -u

import sys
import time
import Ice
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'upper.ice'))
import Example


def get_proxy(ic, str_proxy, cls):
    proxy = ic.stringToProxy(str_proxy)

    for _ in range(3):
        try:
            proxy.ice_ping()
            break
        except Ice.ConnectionRefusedException:
            time.sleep(0.5)

    object = cls.checkedCast(proxy)
    if object is None:
        raise RuntimeError(f'Invalid proxy for {property}')

    return object

def main(ic):
    stringutil = get_proxy(ic, sys.argv[1], Example.StringUtilPrx)
    print(stringutil.upper('Hello World!'))


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
