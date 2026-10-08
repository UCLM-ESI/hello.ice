#!/usr/bin/make -f

NODES     := $(basename $(sort $(wildcard node*.config)))
NODE_DIRS := $(addprefix /tmp/icedata/, $(NODES))

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef


start-grid: /tmp/icedata/registry $(NODE_DIRS)
	reset
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! bash -c ':> /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done

	@for node in $(filter-out node1, $(NODES)); do \
		icegridnode --Ice.Config=$$node.config & \
		echo -- $$node started; \
	done

	@echo -- ok

stop-grid:
	-$(call ig_admin, node shutdown node1)
	@while bash -c ':> /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done
	-killall icegridnode
	@echo -- ok

show-nodes:
	$(call ig_admin, node list)

deploy-app:
	-$(call ig_admin, application remove PrinterApp)
	-$(call ig_admin, application add printerapp-py.xml)
	$(call ig_admin, application update printerapp-py.xml)

distrib-app: deploy-app
	ansible-playbook -i inventory.ini deploy.yml

start-server:
	$(call ig_admin, server start PrinterServer1)

show-server-stdout:
	$(call ig_admin, server show -f PrinterServer1 stdout)

run-client:
	../py/hello/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter" hello

icegridgui:
	GDK_SCALE=2 icegridgui&

/tmp/icedata/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r /tmp/icedata /tmp/printer-py
