#!/usr/bin/make -f

all:

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'

gen-dist: all
	$(RM) -r dist
	mkdir dist
	cp server.py server-uuid.py printer.ice dist/

clean:
	$(RM) *~ proxy.out
	$(RM) -r dist
