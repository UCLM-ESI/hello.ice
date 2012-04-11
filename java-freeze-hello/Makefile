CLASSPATH=-classpath .:/usr/share/java/Ice.jar:/usr/share/java/Freeze.jar:/usr/share/java/db.jar

all: UCLM Client.class Server.class

%.class: %.java
	javac $(CLASSPATH) $<

UCLM: Hello.ice
	slice2java $<


run-server: Server.class db
	java $(CLASSPATH) \
	    Server --Ice.Config=server.cfg | tee server.out

run-client: Client.class
	java $(CLASSPATH) \
	    Client "$(shell head -1 server.out)"

db:
	mkdir db


clean:
	$(RM) *.class server.out *~
	$(RM) -r UCLM db
