all:

clean:
	$(RM) *~ server.proxy

run-server:
	./Server.py --Ice.Config=Server.config | tee server.proxy

run-client:
	./Client.py '$(shell head -1 server.proxy)' 4
