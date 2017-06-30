# -*- mode: makefile-gmake; coding: utf-8 -*-

all:

enter:
	vagrant ssh

run-subscriber:
	if [ -f host.ip ]; then \
	    sed "s/127.0.0.1/$$(cat host.ip)/" subscriber.config > /tmp/subscriber.config; \
	    ./subscriber.py --Ice.Config=/tmp/subscriber.config; \
	else \
	    ./subscriber.py --Ice.Config=subscriber.config; \
	fi
