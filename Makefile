# -*- mode: makefile-gmake; coding: utf-8 -*-

SUBDIRS = $(shell ls -d */)
SUBDIRS = \
	cpp   cpp-icestorm  cpp-ami  cpp-amd  cpp-freeze cpp-observer \
	java java-icestorm java-ami java-amd java-freeze \
	py     py-icestorm   py-ami   py-amd \
	csharp

all:     RULE = all
install: RULE = install
clean:   RULE = clean

all clean install: subdirs

check: all
	atheist .

clean:
	$(RM) *~
	find -name "*.bz2" | xargs --verbose rm -v
	find -name "IcePatch2.sum" | xargs --verbose rm -v
	find -name db | xargs --verbose rm -v -rf


.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(RULE)
