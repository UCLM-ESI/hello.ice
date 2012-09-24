
all:

clean:
	$(RM) *~
	$(RM) -r db

start:  icebox.config icestorm.config
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	sleep 3
	icestormadmin --Ice.Config=icestorm.config -e "create PrinterTopic"

stop: icestorm.config
	icestormadmin --Ice.Config=icestorm.config -e "destroy PrinterTopic"
	killall icebox

run-publisher:  icestorm.config
	./publisher.py --Ice.Config=publisher.config

run-subscriber: icestorm.config
	./subscriber.py --Ice.Config=subscriber.config
