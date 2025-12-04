#!/usr/bin/make -f

IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass
NODES=$(basename $(shell ls node*.config | sort -r))
NODE_DIRS=$(addprefix /tmp/icedata/, $(NODES))

start-grid: /tmp/icedata/registry $(NODE_DIRS)
	cp default-templates.xml /tmp/icedata/
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! ss -ltnH 2>/dev/null | grep -q ':4061'; do sleep 1; done

	@for node in $(filter-out node1, $(NODES)); do \
		icegridnode --Ice.Config=$$node.config & \
		echo -- $$node started; \
	done

	@echo -- ok

stop-grid:
	-$(IG_ADMIN) -e "node shutdown node1"
	@while ss -ltnH | grep -q ":4061"; do sleep 1; done
	-killall icegridnode
	@echo -- ok

show-nodes:
	$(IG_ADMIN) -e "node list"

/tmp/icedata/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r /tmp/db
