

start: /tmp/db/registry /tmp/db/node1 /tmp/db/node2
	icegridnode --Ice.Config=node1.cfg &
	sleep 3
	icegridnode --Ice.Config=node2.cfg &
	icegrid-gui --Ice.Config=locator.cfg

stop:
	killall icegridnode || true

/tmp/db/%:
	mkdir -p $@

clean: stop
	$(RM) *~
	$(RM) -r /tmp/db
