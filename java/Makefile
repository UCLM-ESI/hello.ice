#!/usr/bin/make -f
# -*- mode:makefile -*-

CLASSPATH=-classpath .:/usr/share/java/Ice.jar

all: Example Server.class Client.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: Printer.ice
	slice2java $<

dist:
	mkdir dist

gen-dist: all dist
	cp -r *.class Example dist/
	icepatch2calc dist/

clean:
	$(RM) *.class proxy.out *~
	$(RM) -r Example
	$(RM) -r dist

run-server: Server.class
	java $(CLASSPATH) \
	    Server --Ice.Config=Server.config | tee proxy.out

run-client: Client.class
	java $(CLASSPATH) \
	    Client '$(shell head -1 proxy.out)'
