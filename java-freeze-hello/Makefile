CLASSPATH=-classpath .:/usr/share/java/Ice.jar:/usr/share/java/Freeze.jar:/usr/share/java/libdb4.7-java.jar

all: Client.class Server.class

Server.class: Server.java Hello.java
Client.class: Client.java Hello.java

%.class:
	javac $(CLASSPATH) $<

%.java: %.ice
	slice2java $<


run-server: Server db
	./Server --Ice.Config=config | tee server.out

run-client: Client
	./Client "$(shell head -1 server.out)"

db:
	mkdir db


clean:
	$(RM) *.class server.out *~
	$(RM) -r UCLM db
