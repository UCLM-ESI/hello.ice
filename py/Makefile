#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

dist:
	mkdir dist

gen-dist: dist
	cp Client.py Server.py Server-UUID.py Printer.ice dist/
	icepatch2calc dist/

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist

run-server:
	./Server.py --Ice.Config=Server.config | tee proxy.out

run-client:
	./Client.py '$(shell head -1 proxy.out)'
