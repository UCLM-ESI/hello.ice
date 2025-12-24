#!/usr/bin/make -f

NODES     := $(basename $(sort $(wildcard node*.config)))
NODE_DIRS := $(addprefix /tmp/icedata/, $(NODES))

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef


grid-start: /tmp/icedata/registry $(NODE_DIRS)
	reset
	cp default-templates.xml /tmp/icedata/
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! bash -c ':> /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done

	@for node in $(filter-out node1, $(NODES)); do \
		icegridnode --Ice.Config=$$node.config & \
		echo -- $$node started; \
	done

	@echo -- ok

grid-stop:
	-$(call ig_admin, node shutdown node1)
	@while bash -c ':> /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done
	-killall icegridnode
	@echo -- ok

show-nodes:
	$(call ig_admin, node list)

app-deploy: ../py/dist/IcePatch2.sum
	-$(call ig_admin, application add printerapp-py.xml)
	$(call ig_admin, application update printerapp-py.xml)

app-distrib: app-deploy
	$(call ig_admin, application patch PrinterApp)

server-start:
	$(call ig_admin, server start PrinterServer1)

show-server-stdout:
	$(call ig_admin, server show -f PrinterServer1 stdout)

run-client:
	../py/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter" hello

icegrridgui:
	GDK_SCALE=2 icegridgui&

../py/dist/IcePatch2.sum:
	cd ../py && $(MAKE) gen-dist

/tmp/icedata/%:
	mkdir -p $@

clean: grid-stop
	-$(RM) *~
	-$(RM) -r /tmp/icedata ../py/dist
