#!/usr/bin/make -f
# -*- mode:makefile -*-

start: ./tmp/db/registry ./tmp/db/node1
	icegridnode --Ice.Config=node1.config

./tmp/db/%:
	mkdir -p $@


clean:
	$(RM) *~
	$(RM) -r ./tmp
