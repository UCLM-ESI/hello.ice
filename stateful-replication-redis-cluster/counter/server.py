#!/usr/bin/env -S python3 -u

import sys
import logging
import Ice
from pathlib import Path
import time
from redis.cluster import RedisCluster, ClusterNode

Ice.loadSlice(str(Path(__file__).parent / 'counter.ice'))
import Example

logger = logging.getLogger('CounterServer')
logging.basicConfig(level=logging.INFO)

# one key per counter, so that Redis Cluster spreads them among its masters
PREFIX = 'counter:'


class CounterI(Example.Counter):
    def __init__(self, cluster_nodes):
        if not cluster_nodes:
            raise ValueError("At least one Cluster node must be provided")

        # redis-py's RedisCluster expects startup_nodes as list of dicts or ClusterNode objects,
        # or simply host/port if using host/port args.
        # But commonly we can pass startup_nodes=[{'host': '...', 'port': '...'}, ...]
        # Let's parse the simple host names assuming default port 6379

        startup_nodes = [ClusterNode(host, 6379) for host in cluster_nodes]

        # Retry logic for initial connection
        for _ in range(10):
            try:
                self.redis = RedisCluster(
                    startup_nodes=startup_nodes,
                    decode_responses=True,
                    socket_timeout=5.0,
                    socket_connect_timeout=5.0
                )
                self.redis.ping()
                break
            except Exception as e:
                logger.warning(f"Failed to connect to Redis Cluster: {e}. Retrying...")
                time.sleep(1.0)
        else:
            raise RuntimeError("Redis Cluster not available")

        logger.info("Connected to Redis Cluster")

    def create(self, name, current=None):
        logger.info(f"Received request to create counter: {name}")

        created = self.redis.set(PREFIX + name, 0, nx=True)  # set only if not exists
        if not created:
            logger.info(f"Counter {name} already exists")

    def increment(self, name, delta, current=None):
        logger.info(f"Received request to increment {name} by {delta}")

        # Check existence first
        if not self.redis.exists(PREFIX + name):
            raise Example.NotFound(name)

        # Atomic increment
        self.redis.incrby(PREFIX + name, delta)

    def get(self, name, current=None):
        logger.info(f"Received request to get counter: {name}")

        value = self.redis.get(PREFIX + name)
        if value is None:
            raise Example.NotFound(name)

        return int(value)

    def list(self, current=None):
        logger.info("Received request to list counters")

        # the keys are in several masters: SCAN all of them, and get the
        # values with one MGET per hash slot (so, not atomically)
        keys = list(self.redis.scan_iter(match=PREFIX + '*'))
        values = self.redis.mget_nonatomic(keys)
        return {k[len(PREFIX):]: int(v) for k, v in zip(keys, values)}


def main(ic):
    cluster_nodes = ic.getProperties().getPropertyAsList('Redis.ClusterNodes')
    print(f"Connecting to Redis Cluster nodes at: {cluster_nodes}")

    servant = CounterI(cluster_nodes)
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
