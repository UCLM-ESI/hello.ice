#!/bin/bash
# Each container runs a single IceGrid node (add a container for every new
# node). The ZeroC image only provides the data directory "node1", so every node
# uses that one, each in its own container. If a public key is mounted (see
# icegrid-docker-deploy), start the SSH server too, so that Ansible can copy the
# programs. Then start the node by means of the entrypoint of the ZeroC image.
set -e

if [ "$1" = "icegridnode" ] && [ -f /run/authorized_key.pub ]; then
    install -m 644 /run/authorized_key.pub /etc/ssh/authorized_keys/ice
    /usr/sbin/sshd
fi

exec /docker-entrypoint.sh "$@"
