#!/usr/bin/make -f

CLASSPATH=-classpath .:/usr/share/java/ice-3.7.10.jar

all: Example Server.class ServerUUID.class Client.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: printer.ice
	slice2java $<

dist:
	mkdir dist

gen-dist: clean all dist
	cp -r *.class Example dist/
	icepatch2calc dist/
	ln -sf $(CURDIR)/dist /tmp/printer-server-java

clean:
	$(RM) *.class proxy.out *~
	$(RM) -r Example
	$(RM) -r dist /tmp/printer-server-java

run-server: Server.class
	java $(CLASSPATH) \
		Server --Ice.Config=server.config | tee proxy.out

run-client: Client.class
	java $(CLASSPATH) \
		Client '$(shell head -1 proxy.out)'
