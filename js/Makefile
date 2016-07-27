#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

run-server: BidirAdapter.js
	@echo "Open http://localhost:8080"
	python3 -m http.server 8080

BidirAdapter.js:
	slice2js -I /usr/share/slice BidirAdapter.ice
	cat BidirAdapterHelper.js.in >> $@
