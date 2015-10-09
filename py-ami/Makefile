
all:

clean:
	$(RM) *~ server.proxy

run-server:
	./Server.py --Ice.Config=Server.config | tee server.proxy

run-client-end:
	./Client-end.py '$(shell head -1 server.proxy)' 4

run-client-callback:
	./Client-callback.py '$(shell head -1 server.proxy)' 4
