#!/usr/bin/make -f
# -*- mode:makefile -*-

IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

start: ./tmp/db/registry ./tmp/db/node1
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! netstat -lptn 2> /dev/null | grep ":4061" > /dev/null; do \
	    sleep 1; \
	done

stop:
	$(IG_ADMIN) -e "node shutdown node1"

add-app: app.xml
	$(IG_ADMIN) -e "application add app.xml"

rm-app:
	$(IG_ADMIN) -e "application remove App"

run-client:
	./client.py --Ice.Config=locator.config factory

./tmp/db/%:
	mkdir -p $@

clean:
	$(RM) *~
	$(RM) -r ./tmp
	find -name "*.out" -exec rm {} \;
	find -name "*.err" -exec rm {} \;
