#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

dist:
	mkdir dist

gen-dist: clean dist
	cp client.py server.py server-uuid.py printer.ice dist/
	icepatch2calc dist/
	ln -sf $(PWD)/dist /tmp/printer-server-py

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist /tmp/printer-server-py

run-server:
	./server.py server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'
