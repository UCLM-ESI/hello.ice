#!/usr/bin/make -f

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'

dist:
	mkdir dist

gen-dist: clean dist
	cp server.py server-uuid.py printer.ice dist/
	icepatch2calc dist/
	ln -sf $(PWD)/dist /tmp/printer-py

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist /tmp/printer-py
