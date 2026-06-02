#!/bin/bash
set -e

# Wait for Sentinel to be available and get the current master
MASTER_IP=""
MASTER_PORT="6379"
SENTINEL_HOST="${SENTINEL_HOST:-sentinel-1}"
SENTINEL_PORT="${SENTINEL_PORT:-26379}"
MAX_RETRIES=30
RETRY_COUNT=0

while [ -z "$MASTER_IP" ] && [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  echo "Trying to get master from Sentinel at $SENTINEL_HOST:$SENTINEL_PORT..."
  MASTER_INFO=$(redis-cli -h "$SENTINEL_HOST" -p "$SENTINEL_PORT" SENTINEL get-master-addr-by-name mymaster 2>/dev/null || true)

  if [ ! -z "$MASTER_INFO" ]; then
    # SENTINEL returns: ip port
    MASTER_IP=$(echo "$MASTER_INFO" | head -1)
    MASTER_PORT=$(echo "$MASTER_INFO" | tail -1)
    echo "Found master: $MASTER_IP:$MASTER_PORT"
  else
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Sentinel not ready yet, retrying... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 1
  fi
done

if [ -z "$MASTER_IP" ]; then
  echo "ERROR: Could not get master address from Sentinel after $MAX_RETRIES retries"
  exit 1
fi

# Start Redis with dynamic master configuration
echo "Starting Redis replicating from $MASTER_IP:$MASTER_PORT"
redis-server \
  --replicaof "$MASTER_IP" "$MASTER_PORT" \
  --repl-diskless-load on-empty-db \
  --protected-mode no \
  "$@"
