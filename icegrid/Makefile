#!/usr/bin/make -f
# -*- mode:makefile -*-

NODES=$(basename $(shell ls node*.config | sort -r))
NODE_DIRS=$(addprefix /tmp/db/, $(NODES))
IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

start-grid: /tmp/db/registry $(NODE_DIRS)
	cp default-templates.xml /tmp/
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! ss -ltnH 2>/dev/null | grep -q ':4061'; do sleep 1; done

	@for node in $(filter-out node1, $(NODES)); do \
		icegridnode --Ice.Config=$$node.config & \
		echo -- $$node started; \
	done

	@echo -- ok

stop-grid:
	$(IG_ADMIN) -e "node shutdown node1"
	@while ss -ltnH 2>/dev/null | grep -q ':4061'; do sleep 1; done
	killall icegridnode || true
	@echo -- ok

show-nodes:
	$(IG_ADMIN) -e "node list"

/tmp/db/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r /tmp/db
