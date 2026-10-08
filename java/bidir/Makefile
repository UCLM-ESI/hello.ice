#!/usr/bin/make -f

CLASSPATH=-classpath .:/usr/share/java/ice-3.7.10.jar

all: Example Server.class Client.class PrinterI.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: printer.ice callback.ice
	slice2java -I/usr/share/ice/slice $^

gen-dist: all
	$(RM) -r dist
	mkdir dist
	cp -r *.class Example dist/

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
