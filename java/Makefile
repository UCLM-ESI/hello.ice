
all: UCLM Server.class Client.class

%.class: %.java
	javac -classpath /usr/share/java/Ice.jar:. $<

UCLM: ../Hello.ice
	slice2java $<

clean:
	$(RM) *.class proxy.out *~
	$(RM) -r UCLM

run-server: Server.class
	java -classpath .:/usr/share/java/Ice.jar \
		Server --Ice.Config=../hello.cfg | tee proxy.out

run-client: Client.class
	java -classpath .:/usr/share/java/Ice.jar \
	    Client "$(shell head -1 proxy.out)"
