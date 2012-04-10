

start: db/server db/client db/registry
	icegridnode --Ice.Config=node1.cfg &
	sleep 3
	icegridnode --Ice.Config=node2.cfg &
	icegrid-gui --Ice.Config=locator.cfg

stop:
	killall icegridnode

db/%:
	mkdir -p $@

clean: stop
	$(RM) *~
	$(RM) -r db
