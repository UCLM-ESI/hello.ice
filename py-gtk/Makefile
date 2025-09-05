
all:

clean:
	$(RM) *~ proxy.out

run-server:
	./server.py --Ice.Config=../config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'
