# Stateful Replication Demo

This demo showcases a **stateful, replicated counter service** built with ZeroC Ice that uses Redis for persistent state management with high availability through Redis Sentinel.

## Overview

The demo implements a distributed counter service with the following architecture:

- **Ice Grid**: Manages two replicated server instances across different nodes
- **Round-robin group**: Distributes client requests across server instances
- **Redis**: Stores counter state with master-replica replication
- **Redis Sentinel**: Provides high availability and automatic failover for Redis

## Architecture Components

### Ice Services
- **Registry**: IceGrid registry that manages application deployment
- **Node1 & Node2**: Two independent nodes running Counter server instances
- **CounterGroup**: A replica group with round-robin load balancing

### Data Layer
- **Redis Master**: Primary Redis instance storing counters
- **Redis Replicas**: Secondary Redis instances for read scaling (docker `--scale redis-replica=2`)
- **Sentinel**: Redis Sentinel cluster (docker `--scale sentinel=3`) for monitoring and failover

## Directory Structure

```
stateful-replication/
├── compose.yml          # Docker Compose orchestration
├── app.xml              # IceGrid application deployment descriptor
├── Makefile             # Deployment and demo
├── counter/             # Counter service implementation
│   ├── counter.ice      # Slice interface definition
│   ├── server.py        # Server implementation (connects to Redis)
│   └── client.py        # Client implementation for testing
├── docker/              # Docker build context
│   ├── ignode-redis/    # IceGrid node image with Redis client
│   └── sentinel/        # Redis Sentinel configuration
├── registry.config      # IceGrid registry configuration
├── node1.config         # Node1 configuration
├── node2.config         # Node2 configuration
└── locator.config       # Client locator configuration
```

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
- Launches 2 Counter server instances
- Starts Redis master with 2 replicas
- Deploys 3 Redis Sentinel instances for monitoring

### Deploy the Application

```bash
make add-app
```

This registers the Counter application with IceGrid and deploys the server instances.

### Run a Client

```bash
make client
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


## How It Works

1. **Server Initialization**: Each Counter server instance connects to Redis via Sentinel, discovering the current master.
2. **State Management**: All counter data is stored in Redis with automatic replication.
3. **High Availability**: If the Redis master fails, Sentinel automatically promotes a replica.
4. **Service Distribution**: Clients are routed to server instances via IceGrid's round-robin load balancing.
5. **Persistent Storage**: Counter state persists across server restarts thanks to Redis persistence.

## Network Configuration

All services communicate over a custom Docker network (`icegrid`) with the following addressing:
- Registry: `172.28.0.10:4061`
- Node1 & Node2: Dynamic assignment on `icegrid` network
- Redis Master: `redis-master:6379`
- Sentinel: `sentinel:26379` (scaled to 3 instances)

## Use Cases

This demo is ideal for learning about:
- Distributed systems with replication
- High-availability database patterns
- IceGrid deployment and management
- Redis Sentinel failover mechanisms
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

To test Redis Sentinel failover:

```bash
docker compose stop redis-master
```

Sentinel will automatically promote one of the replicas within seconds. The server instances will detect the new master via Sentinel and continue operating without interruption.

## Further Reading

- [ZeroC Ice Documentation](https://zeroc.com/doc/ice/3.7/)
- [IceGrid Reference](https://zeroc.com/doc/ice/3.7/manual/icegrid.html)
- [Redis Sentinel Documentation](https://redis.io/topics/sentinel)

## License

This demo is part of the hello.ice repository.
