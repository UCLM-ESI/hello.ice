#!/usr/bin/make -f

all: printer.js

%.js: %.ice
	slice2js $<

start-glacier:
	glacier2router --Ice.Config=glacier.config

run-server: all
	@echo "Open http://localhost:8080"
	python3 -m http.server 8080

clean:
	$(RM) *~ printer.js
