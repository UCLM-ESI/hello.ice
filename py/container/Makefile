
run-server:
	./server.py --Ice.Config=container.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'
