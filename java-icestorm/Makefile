CLASSPATH=-classpath /usr/share/java/Ice.jar:/usr/share/java/IceStorm.jar:.

all: Example Subscriber.class Publisher.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: Printer.ice
	slice2java $<

clean:
	$(RM) *.class *~
	$(RM) -r Example


run-subscriber: Subscriber.class
	java $(CLASSPATH) Subscriber --Ice.Config=subscriber.config

run-publisher: Publisher.class
	java $(CLASSPATH) Publisher --Ice.Config=publisher.config

start: /usr/bin/icebox /usr/bin/icestormadmin
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	sleep 3
	icestormadmin --Ice.Config=icestorm.config -e "create PrinterTopic"

stop:
	icestormadmin --Ice.Config=icestorm.config -e "destroy PrinterTopic"
	killall icebox
