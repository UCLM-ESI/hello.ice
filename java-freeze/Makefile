CLASSPATH=-classpath /usr/share/java/Ice.jar:/usr/share/java/Freeze.jar:/usr/share/java/db.jar:.
LIBRARYPATH=-Djava.library.path=/usr/lib/i386-linux-gnu

all: Counter Client.class Server.class

%.class: %.java
	javac $(CLASSPATH) $<

Counter: counter.ice
	slice2java $<

clean:
	$(RM) *.class server.out proxy.out *~
	$(RM) -r Counter db

run-server: Server.class db
	java $(LIBRARYPATH) $(CLASSPATH) \
	    Server --Ice.Config=server.cfg | tee server.out

run-client: Client.class
	grep -v "^--" server.out > proxy.out
	java $(LIBRARYPATH) $(CLASSPATH) \
	    Client '$$(head -1 proxy.out)'

db:
	mkdir $@
