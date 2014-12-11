#!/usr/bin/make -f
# -*- mode:makefile -*-

start-grid: /tmp/db/registry /tmp/db/node1 /tmp/db/node2
	icegridnode --Ice.Config=node1.config &
	while ! netstat -lptn 2> /dev/null | grep ":4061"; do sleep 1; done
	icegridnode --Ice.Config=node2.config &
	icegridadmin --Ice.Config=locator.config -uuser -ppass -e "node list"

stop-grid:
	for node in node2 node1; do \
	    icegridadmin --Ice.Config=locator.config -u user -p pass -e "node shutdown $$node"; \
	done
	killall icegridnode

/tmp/db/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r /tmp/db
