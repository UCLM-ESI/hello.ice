clean:
	$(RM) *~
	$(RM) -r db

start: icebox.config icestorm.config
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	@while ! ss -ltnH 2>/dev/null | grep -q ':2000'; do sleep 1; done
	-icestormadmin --Ice.Config=icestorm.config -e "create PrinterTopic"

stop: icestorm.config
	icestormadmin --Ice.Config=$< -e "destroy PrinterTopic"
	killall icebox

run-publisher: publisher.config
	sleep 1
	./publisher.py --Ice.Config=$<

run-subscriber: subscriber.config
	./subscriber.py --Ice.Config=$<
