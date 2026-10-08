#!/usr/bin/make -f

ICEDATA   := /tmp/icedata
NODES     := $(basename $(sort $(wildcard node*.config)))
NODE_DIRS := $(addprefix $(ICEDATA)/, $(NODES))

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef


start-grid: $(ICEDATA)/registry $(NODE_DIRS)
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

load-app:
	$(call ig_admin, application add printerapp.xml) 2>/dev/null || \
	$(call ig_admin, application update printerapp.xml)

deploy:
	ansible-playbook -i inventory.ini deploy.yml

start-servers:
	$(call ig_admin, server start PrinterServer1)
	$(call ig_admin, server start PrinterServer2)

show-server-out:
	$(call ig_admin, server show PrinterServer1 stdout -f)

clean-outs:
	$(RM) /tmp/printer-java/*/server-out.txt /tmp/printer-java/*/server-err.txt

run-client:
	java -classpath ../hello:/usr/share/java/ice-3.7.10.jar \
		Client --Ice.Config=locator.config "printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter"

icegridgui:
	GDK_SCALE=2 icegridgui&

$(ICEDATA)/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r $(ICEDATA) /tmp/printer-java
