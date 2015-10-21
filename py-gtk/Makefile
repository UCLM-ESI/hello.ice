
all:

clean:
	$(RM) *~ proxy.out

run-server:
	./Server.py --Ice.Config=../config | tee proxy.out

run-client:
	./Client.py '$(shell head -1 proxy.out)'
