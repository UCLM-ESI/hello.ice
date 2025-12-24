FROM zeroc/icegridnode:3.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    iproute2 net-tools \
    python3-zeroc-ice zeroc-ice-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
