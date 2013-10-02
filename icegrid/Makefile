

start: /tmp/db/registry /tmp/db/node1 /tmp/db/node2
	icegridnode --Ice.Config=node1.cfg &
	while ! netstat -lptn 2> /dev/null | grep ":4061"; do sleep 1; done
	icegridnode --Ice.Config=node2.cfg &
	icegrid-gui --Ice.Config=locator.cfg

stop:
	killall icegridnode || true

/tmp/db/%:
	mkdir -p $@

clean: stop
	$(RM) *~
	$(RM) -r /tmp/db
