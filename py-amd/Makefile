
all:

clean:
	$(RM) *~ server.proxy

run-server:
	./Server.py --Ice.Config=../hello.cfg | tee server.proxy

run-client:
	./Client.py "$(shell head -1 server.proxy)" 4
