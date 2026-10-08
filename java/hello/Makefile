#!/usr/bin/make -f

CLASSPATH=-classpath .:/usr/share/java/ice-3.7.10.jar

all: build

build: Example Server.class ServerUUID.class Client.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: printer.ice
	slice2java $<

gen-dist: build
	$(RM) -r dist
	mkdir -p dist/Example
	cp Server.class ServerUUID.class PrinterI.class dist/
	cp Example/*.class dist/Example/

clean:
	$(RM) *.class proxy.out *~
	$(RM) -r Example
	$(RM) -r dist

run-server: Server.class
	java $(CLASSPATH) \
		Server --Ice.Config=server.config | tee proxy.out

run-client: Client.class
	java $(CLASSPATH) \
		Client '$(shell head -1 proxy.out)'
