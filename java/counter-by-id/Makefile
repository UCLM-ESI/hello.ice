#!/usr/bin/make -f

CLASSPATH=-classpath .:/usr/share/java/ice-3.7.10.jar

all: Example Server.class Client.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: counter.ice
	slice2java $<

clean:
	$(RM) *.class *~
	$(RM) -r Example

run-server: Server.class
	java $(CLASSPATH) Server --Ice.Config=server.config

run-client: Client.class
	java $(CLASSPATH) Client 'counter1 -t:tcp -h localhost -p 2002'
