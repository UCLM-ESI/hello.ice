
SUBDIRS = \
	cpp   cpp-icestorm  cpp-ami  cpp-amd  \
	py    py-icestorm   py-ami   py-amd \
	java  java-icestorm java-ami java-amd \
	cpp-observer php py-counter-by-identity py-protobuff

all:     RULE = all
install: RULE = install
clean:   RULE = clean

all clean install: subdirs

check: export PYTHONPATH = $(shell pwd)
check: all
	find -name "test.py" | xargs prego -- --import-mode=importlib

clean:
	$(RM) *~
	find -name "*.bz2" | xargs --verbose rm -fv
	find -name "IcePatch2.sum" | xargs --verbose rm -fv
	find -name db | xargs --verbose rm -vrf
	find -name *.orig | xargs --verbose rm -vrf
	find -name "*.pyc" | xargs --verbose rm -vrf
	find -name "*_flymake.py" | xargs --verbose rm -vrf
	find -name "__pycache__" | xargs --verbose rm -vrf


.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(RULE)
