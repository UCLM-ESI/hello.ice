
all:

clean:
	$(RM) *~ server.proxy

run-server:
	./server.py --Ice.Config=server.config | tee server.proxy

run-client-block:
	./client-block.py '$(shell head -1 server.proxy)' 4

run-client-callback:
	./client-callback.py '$(shell head -1 server.proxy)' 4

run-client-await:
	./client-await.py '$(shell head -1 server.proxy)' 4
