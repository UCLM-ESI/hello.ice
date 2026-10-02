
SUBDIRS = \
	cpp/hello   cpp/icestorm  cpp/ami  cpp/amd  \
	py/hello    py/icestorm   py/ami   py/amd \
	java/hello  java/icestorm java/ami java/amd \
	cpp/observer php py/counter-by-id py/protobuff \
	cpp/counter-by-id cpp/counter-by-key java/counter-by-id java/counter-by-key

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
	find -name db -type d -prune -exec git clean -fdX -- {} +
	find -name "*.orig" | xargs --verbose rm -vrf
	find -name "*.pyc" | xargs --verbose rm -vrf
	find -name "*_flymake.py" | xargs --verbose rm -vrf
	find -name "__pycache__" | xargs --verbose rm -vrf


.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(RULE)
