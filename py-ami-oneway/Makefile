#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

dist:
	mkdir dist

gen-dist: dist
	cp client.py server.py printer.ice dist/
	icepatch2calc dist/

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'
