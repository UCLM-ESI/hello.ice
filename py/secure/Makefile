#!/usr/bin/make -f

all:

gen-dist:
	$(RM) -r dist
	mkdir dist
	cp client.py server.py server-uuid.py printer.ice dist/
	ln -sfn $(CURDIR)/dist /tmp/printer-server-py

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist /tmp/printer-server-py

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py --Ice.Config=Client.config '$(shell head -1 proxy.out)'
