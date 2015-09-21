#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

dist:
	mkdir dist

gen-dist: dist
	cp Client.py Server.py Printer.ice Callback.ice dist/
	icepatch2calc dist/

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist

run-server:
	./Server.py --Ice.Config=Server.config
