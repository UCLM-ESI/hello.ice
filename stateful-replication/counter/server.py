#!/usr/bin/env -S python3 -u

import sys
import logging
import Ice
from pathlib import Path
import time
from redis.sentinel import Sentinel

Ice.loadSlice(str(Path(__file__).parent / 'counter.ice'))
import Example

logger = logging.getLogger('CounterServer')
logging.basicConfig(level=logging.INFO)


class CounterI(Example.Counter):
    def __init__(self, sentinel_hosts):
        if not sentinel_hosts:
            raise ValueError("At least one Sentinel host must be provided")
        sentinels_endpoints = [(host, 26379) for host in sentinel_hosts]
        sentinel = Sentinel(
            sentinels_endpoints, socket_timeout=5.0, socket_connect_timeout=5.0)

        for _ in range(10):
            try:
                self.redis = sentinel.master_for(
                    service_name='mymaster',
                    socket_timeout=5.0,
                    socket_connect_timeout=5.0,
                    socket_keepalive=True,
                    retry_on_timeout=True,
                    decode_responses=True
                )
                self.redis.ping()
                break
            except Exception:
                time.sleep(0.5)

        else:
            raise RuntimeError("Redis master not available")

        self.key = "counters"

        logger.info("Connected to Redis master via Sentinel")

    def create(self, name, current=None):
        logger.info(f"Received request to create counter: {name}")

        created = self.redis.hsetnx(self.key, name,  0)  # HSETNX: set only if not exists
        if not created:
            logger.info(f"Counter {name} already exists")

    def increment(self, name, delta, current=None):
        logger.info(f"Received request to increment {name} by {delta}")

        # Check existence first
        if not self.redis.hexists(self.key, name):
            raise Example.NotFound(name)

        # Atomic increment
        self.redis.hincrby(self.key, name, delta)

    def get(self, name, current=None):
        logger.info(f"Received request to get counter: {name}")

        value = self.redis.hget(self.key, name)
        if value is None:
            raise Example.NotFound(name)

        return int(value)

    def list(self, current=None):
        logger.info("Received request to list counters")

        # Returns dict[str, str] → convert to dict[str, int]
        data = self.redis.hgetall(self.key)
        return {k: int(v) for k, v in data.items()}


def main(ic):
    sentinels = ic.getProperties().getPropertyAsList('Redis.Sentinels')
    print(f"Connecting to Redis Sentinels at: {sentinels}")

    servant = CounterI(sentinels)
    adapter = ic.createObjectAdapter('CounterAdapter')
    proxy = adapter.add(servant, ic.stringToIdentity('counter'))
    print(proxy)

    adapter.activate()
    ic.waitForShutdown()
    return 0


if __name__ == '__main__':
    try:
        with Ice.initialize(sys.argv) as communicator:
            sys.exit(main(communicator))
    except KeyboardInterrupt:
        print("Shutting down server...")
