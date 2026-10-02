#!/usr/bin/make -f

all: printer.js callback.js

%.js: %.ice
	slice2js -I/usr/share/ice/slice $<

run-server: all
	@echo "Open http://localhost:8080"
	python3 -m http.server 8080

clean:
	$(RM) *~ printer.js callback.js
