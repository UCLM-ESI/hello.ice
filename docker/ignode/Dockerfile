# IceGrid node for every example that runs in docker containers: the ZeroC
# image plus what their servers and tools need (Ice for Python, icegridadmin,
# IceBox and IceStorm, the Redis client and the SSH server used by Ansible)
FROM zeroc/icegridnode:3.7

# the Redis client of the distribution is too old for RedisCluster
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-zeroc-ice python3-pip \
    zeroc-ice-utils zeroc-icebox libzeroc-icestorm3.7 \
    openssh-server iproute2 net-tools && \
    pip3 install --no-cache-dir redis && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /run/sshd /etc/ssh/authorized_keys

COPY sshd.conf /etc/ssh/sshd_config.d/icegrid.conf
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["icegridnode", "--Ice.Config=/etc/icegridnode.conf"]
