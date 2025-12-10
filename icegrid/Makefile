#!/usr/bin/make -f

NODES     := $(basename $(sort $(wildcard node*.config)))
NODE_DIRS := $(addprefix /tmp/icedata/, $(NODES))

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef


start-grid: /tmp/icedata/registry $(NODE_DIRS)
	cp default-templates.xml /tmp/icedata/
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! bash -c 'echo > /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done

	@for node in $(filter-out node1, $(NODES)); do \
		icegridnode --Ice.Config=$$node.config & \
		echo -- $$node started; \
	done

	@echo -- ok

stop-grid:
	-$(call ig_admin, node shutdown node1)
	@while bash -c 'echo > /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done
	-killall icegridnode
	@echo -- ok

show-nodes:
	$(call ig_admin, node list)

/tmp/icedata/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r /tmp/icedata
