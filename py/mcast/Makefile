#!/usr/bin/make -f

all:

gen-dist:
	$(RM) -r dist
	mkdir dist
	cp client.py server.py printer.ice dist/

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'
