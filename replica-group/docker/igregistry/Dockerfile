FROM zeroc/icegridregistry:3.7

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    iproute2 net-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
