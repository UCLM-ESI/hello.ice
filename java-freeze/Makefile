CLASSPATH=-classpath .:/usr/share/java/Ice.jar:/usr/share/java/Freeze.jar:/usr/share/java/libdb5.1-java.jar

all: Client.class Server.class

Server.class: Server.java counter.java
Client.class: Client.java counter.java

%.class:
	javac $(CLASSPATH) $<

%.java: %.ice
	slice2java $<

clean:
	$(RM) *.class server.out *~
	$(RM) -r Counter db

run-client: Client.class
	java $(CLASSPATH) \
	    Client "$(shell head -1 proxy.out)"

run-server: Server.class db
	java $(CLASSPATH) \
	    Server --Ice.Config=hello.cfg | tee proxy.out

db:
	mkdir $@
