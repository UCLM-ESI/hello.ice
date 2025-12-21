FROM zeroc/icegridnode:3.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-zeroc-ice python3-redis iproute2 net-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
