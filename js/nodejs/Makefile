# -*- mode: makefile; coding: utf-8 -*-

ICEJS           = ../IceJS
SLICE2JS        = $(ICEJS)/bin/slice2js
LD_LIBRARY_PATH = $(ICEJS)/lib

export LD_LIBRARY_PATH

all: Printer.js

Printer.js: Printer.ice
	$(SLICE2JS) $^


.PHONY: clean
clean:
	$(RM) -f Printer.js
