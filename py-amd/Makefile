all:

clean:
	$(RM) *~ server.proxy

run-server:
	PYTHONUNBUFFERED=1 ./Server.py --Ice.Config=Server.config | tee server.proxy

run-client:
	./Client.py '$(shell head -1 server.proxy)' 4
