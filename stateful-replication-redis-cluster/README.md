# Stateful Replication Demo (Redis Cluster)

This demo showcases a **stateful, replicated counter service** built with ZeroC Ice that stores its state in a **Redis Cluster**. It is a variant of [stateful-replication](../stateful-replication), which uses a Redis master with replicas supervised by Sentinel instead.

## Overview

The demo implements a distributed counter service with the following architecture:

- **Ice Grid**: Manages two replicated server instances across different nodes
- **Round-robin group**: Distributes client requests across server instances
- **Redis Cluster**: Stores counter state in 3 masters, each one with a replica
- **Failover**: The cluster itself detects a failed master and promotes its replica (no Sentinel)

## Architecture Components

### Ice Services
- **Registry**: IceGrid registry that manages the application
- **Node1 & Node2**: Two independent nodes running Counter server instances
- **CounterGroup**: A replica group with round-robin load balancing

### Data Layer
- **Redis nodes** (`redis-node-1` ... `redis-node-6`): Redis instances in cluster mode
- **cluster-creator**: One-shot container that runs `redis-cli --cluster create ... --cluster-replicas 1`, which joins the 6 nodes into a cluster of 3 masters and 3 replicas. node1 and node2 wait until it finishes.

The Counter servers get some cluster nodes as entry points (property `Redis.ClusterNodes` in app.xml), and the Redis client discovers the rest of the cluster from them.

## Directory Structure

```
stateful-replication-redis-cluster/
├── compose.yml          # Docker Compose orchestration
├── app.xml              # IceGrid application descriptor
├── Makefile             # Targets to run the demo
├── counter/             # Counter service implementation
│   ├── counter.ice      # Slice interface definition
│   ├── server.py        # Server implementation (connects to Redis Cluster)
│   └── client.py        # Client implementation for testing
├── registry.config      # IceGrid registry configuration
├── node1.config         # Node1 configuration
├── node2.config         # Node2 configuration
└── locator.config       # Client locator configuration
```

The IceGrid nodes use the image in `../docker/ignode`, shared by all the examples that run in Docker (it includes the Redis client).

## Counter Interface

The service provides the following operations:

```ice
interface Counter {
    void create(string name);                          // Create a new counter
    void increment(string name, long delta);           // Increment counter by delta
    long get(string name);                             // Get current counter value
    CounterDict list();                                // List all counters
}
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.x (for client)

### Bring Up the Demo

```bash
make up
```

This command:
- Starts the IceGrid registry
- Starts 6 Redis nodes and creates the cluster
- Starts 2 IceGrid nodes (node1, node2)

### Load the Application

```bash
make load-app
```

This adds the Counter application (app.xml) to the IceGrid Registry. The Counter servers are activated on demand, with the first request.

### Run a Client

```bash
make run-client
```

This executes the test client which:
1. Creates a counter named "counter1"
2. Increments it by 5
3. Prints the current value

### View Logs

```bash
make logs
```

Monitor the output from all containers in real-time.

### View the Cluster

```bash
make cluster-status
```

Shows the cluster nodes, their role (master or slave) and the hash slots of each master.


## How It Works

1. **Server Initialization**: Each Counter server connects to the cluster through the nodes in `Redis.ClusterNodes`.
2. **State Management**: Each counter is a Redis key (`counter:<name>`). Redis Cluster assigns each key to one of its 16384 hash slots, so the counters are spread among the 3 masters. `list()` scans all of them.
3. **High Availability**: If a master fails, the cluster promotes its replica after `cluster-node-timeout` (5 seconds).
4. **Service Distribution**: Clients are routed to server instances via IceGrid's round-robin load balancing.

## Network Configuration

All services communicate over a custom Docker network (`icegrid`) with the following addressing:
- Registry: `172.28.0.10:4061`
- Node1 & Node2: Dynamic assignment on `icegrid` network
- Redis nodes: `redis-node-1` ... `redis-node-6`, `172.28.0.21` ... `172.28.0.26`, port `6379`

## Use Cases

This demo is ideal for learning about:
- Distributed systems with replication
- High-availability database patterns
- IceGrid application management
- Redis Cluster failover mechanisms
- Stateful microservices architecture

## Testing Failure Scenarios

You can stop individual containers to test fault tolerance:

### Test Node Failure

Stop a server node to verify failover to the replica:
```bash
docker compose stop node1
```
Then run the client again - requests should automatically route to node2.

### Test Redis Master Failure

After running the client at least once, find the master that holds `counter1`:

```bash
docker compose exec redis-node-1 redis-cli -c get counter:counter1
```

With `-c`, redis-cli follows the cluster redirection and prints the node that holds the key (`-> Redirected to slot [...] located at 172.28.0.2X:6379`). If there is no redirection, the key is in redis-node-1 itself.

Stop that master (`172.28.0.2X` is `redis-node-X`):

```bash
docker compose stop redis-node-X
```

After `cluster-node-timeout` (5 seconds) the cluster promotes its replica. Check it with `make cluster-status` (it queries redis-node-1, so if you stopped that one, run `redis-cli cluster nodes` in another node) and run the client again.

## Further Reading

- [ZeroC Ice Documentation](https://zeroc.com/doc/ice/3.7/)
- [IceGrid Reference](https://zeroc.com/doc/ice/3.7/manual/icegrid.html)
- [Redis Cluster Tutorial](https://redis.io/topics/cluster-tutorial)

## License

This demo is part of the hello.ice repository.
