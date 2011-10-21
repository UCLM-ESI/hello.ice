
clean:
	$(RM) *~
	$(RM) -r db

run-publisher:  icestorm.config
	./publisher.py --Ice.Config=icestorm.config

run-subscriber: icestorm.config
	./subscriber.py --Ice.Config=icestorm.config

start:  icebox.config icestorm.config
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	sleep 3
	icestormadmin --Ice.Config=icestorm.config -e "create HelloTopic"

stop: icestorm.config
	icestormadmin --Ice.Config=icestorm.config -e "destroy HelloTopic"
	killall icebox
