CLASSPATH=-classpath /usr/share/java/Ice.jar:.

all: Example Server.class Client_end.class

%.class: %.java
	javac $(CLASSPATH) $<

Example: factorial.ice
	slice2java $<

clean:
	$(RM) *.class proxy.out *~
	$(RM) -r Example

run-server: Server.class
	java $(CLASSPATH) \
		Server --Ice.Config=hello.cfg | tee proxy.out

run-client-end: Client_end.class
	java $(CLASSPATH) \
	    Client_end "$(shell head -1 proxy.out)" 6
