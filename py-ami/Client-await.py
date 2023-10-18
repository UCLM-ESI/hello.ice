#!/usr/bin/env -S python3 -u
# -*- coding: utf-8 -*-

import sys
import asyncio

import Ice
Ice.loadSlice('./factorial.ice')
import Example


class Server:
    async def main(self):
        with Ice.initialize(sys.argv) as broker:
            return await self.run(broker)

    async def run(self, broker):
        proxy = broker.stringToProxy(sys.argv[1])
        math = Example.MathPrx.checkedCast(proxy)
        value = int(sys.argv[2])

        if not math:
            raise RuntimeError("Invalid proxy")

        result = await Ice.wrap_future(math.factorialAsync(value))
        print(f"Async result is: {result}")

        return 0


sys.exit(asyncio.run(Server().main()))
