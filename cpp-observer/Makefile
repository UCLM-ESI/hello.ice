LDLIBS=-lIce -lIceUtil -lFreeze -lIceStorm
CXXFLAGS=-I.

SLICES=$(wildcard *.ice)
GENERATED=$(SLICES:.ice=.cpp) $(SLICES:.ice=.h)
TARGET=Factory Create Modify Monitor

all: $(TARGET)

Factory: Factory.o Bool.o BoolPersistent.o BoolFactory.o
Factory.o: Factory.cpp Bool.h BoolPersistent.h BoolFactory.h

Create: Create.o BoolFactory.o
Create.o: Create.cpp BoolFactory.h

Modify: Modify.o Bool.o
Modify.o: Modify.cpp Bool.h

Monitor: Monitor.o Bool.o BoolPersistent.o
Monitor.o: Monitor.cpp BoolPersistent.h Bool.h

%.h %.cpp: %.ice
	slice2cpp -I/usr/share/Ice/slice $<

clean:
	$(RM) $(TARGET)
	$(RM) *.o *~ $(GENERATED)
	$(RM) -rf db

	$(RM) factory.proxy obj.proxy

db/%:
	mkdir -p $@

start: db/icestorm /usr/bin/icebox /usr/bin/icestormadmin
	icebox --Ice.Config=icebox.config &

stop:
	-killall icebox
	-killall Factory
	sleep 2
	$(RM) -r db

run-factory: Factory
	./Factory --Ice.Config=factory.cfg > factory.proxy &

run-create: factory.proxy
	./Create "$$(cat factory.proxy)" > obj.proxy

run-monitor: Monitor obj.proxy
	@echo Keep this console open
	./Monitor --Ice.Config=monitor.cfg "$$(cat obj.proxy)"

run-modify: Modify
	./Modify "$$(cat obj.proxy)" true
	./Modify "$$(cat obj.proxy)" false
