
all:

clean:
	$(RM) *~ server.proxy

run-server:
	./Server.py --Ice.Config=Server.config | tee server.proxy

run-client-block:
	./Client-block.py '$(shell head -1 server.proxy)' 4

run-client-callback:
	./Client-callback.py '$(shell head -1 server.proxy)' 4

run-client-await:
	./Client-await.py '$(shell head -1 server.proxy)' 4
