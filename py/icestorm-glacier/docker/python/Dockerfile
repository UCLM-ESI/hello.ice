FROM debian:trixie-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-zeroc-ice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
