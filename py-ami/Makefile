
all:

clean:
	$(RM) *~ proxy.out

run-server:
	./Server.py --Ice.Config=../hello.cfg | tee proxy.out

run-client:
	./Client.py "$(shell head -1 proxy.out)"
