#!/usr/bin/make -f
# -*- mode:makefile -*-


start: /tmp/db/registry /tmp/db/node1 /tmp/db/node2
	icegridnode --Ice.Config=node1.cfg &
	while ! netstat -lptn 2> /dev/null | grep ":4061"; do sleep 1; done
	icegridnode --Ice.Config=node2.cfg &
	icegridadmin --Ice.Config=locator.cfg -uuser -ppass -e "node list"

stop:
	for node in ClientNode ServerNode; do \
	    icegridadmin --Ice.Config=node2.cfg -u user -p pass -e "node shutdown $$node"; \
	done

/tmp/db/%:
	mkdir -p $@

clean: stop
	$(RM) *~
	$(RM) -r /tmp/db
