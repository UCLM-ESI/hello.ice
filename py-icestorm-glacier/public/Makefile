# -*- mode: makefile-gmake; coding: utf-8 -*-

all:

run-glacier:
	glacier2router --Ice.Config=glacier.config

run-icestorm: save-ip-address
	rm -fr /tmp/py-icestorm-glacier-db; mkdir -p /tmp/py-icestorm-glacier-db
	icebox --Ice.Config=icestorm.config

run-publisher:
	./publisher.py --Ice.Config=publisher.config


# this ip will be the 'public' ip for private machine
save-ip-address:
	 ip a | 'grep' " inet " | 'grep' -v "127.0.0" | \
	    sed 's/^ *//' | cut -d" " -f 2 | cut -d"/" -f 1 \
	    > ../private/host.ip
