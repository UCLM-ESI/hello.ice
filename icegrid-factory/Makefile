#!/usr/bin/make -f
# -*- mode:makefile -*-

IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

start: ./tmp/db/registry ./tmp/db/node1
	icegridnode --Ice.Config=node1.config &

stop:
	$(IG_ADMIN) -e "node shutdown node1"

./tmp/db/%:
	mkdir -p $@

add-app: app.xml
	$(IG_ADMIN) -e "application add app.xml"

clean: stop
	$(RM) *~
	$(RM) -r ./tmp
	find -name "*.out" -exec rm {} \;
	find -name "*.err" -exec rm {} \;
