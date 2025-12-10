#!/usr/bin/make -f

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef

start: ./tmp/db/registry ./tmp/db/node1
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! bash -c 'echo > /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done
	@echo -- ok

stop:
	-$(call ig_admin, node shutdown node1)
	@while bash -c 'echo > /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 1; done
	-killall icegridnode
	@echo -- ok

rm-app:
	-$(call ig_admin, application remove App)

add-app: start rm-app app.xml
	$(call ig_admin, application add app.xml)

run-client:
	./client.py --Ice.Config=locator.config factory

./tmp/db/%:
	mkdir -p $@

clean:
	-@$(MAKE) stop
	$(RM) -r *~ ./tmp
	find . \( -name "*.out" -o -name "*.err" \) -exec rm {} \;
