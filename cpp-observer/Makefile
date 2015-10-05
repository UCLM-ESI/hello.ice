#!/usr/bin/make -f
# -*- mode:makefile -*-

include ../cpp-common.mk

LDLIBS += -lFreeze -lIceStorm

SLICES=$(wildcard *.ice)
GENERATED=$(SLICES:.ice=.cpp) $(SLICES:.ice=.h)
TARGET=Server Create Modify Monitor

all: $(TARGET)

Server: Server.o Bool.o BoolPersistent.o BoolFactory.o
Server.o: Server.cpp Bool.h BoolPersistent.h BoolFactory.h

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

	$(RM) server.proxy obj.proxy

db/%:
	mkdir -p $@

start: db/icestorm /usr/bin/icebox /usr/bin/icestormadmin
	icebox --Ice.Config=icebox.config &

stop:
	-killall icebox
	-killall Server
	sleep 2
	$(RM) -r db

run-server: Server
	./Server --Ice.Config=server.cfg > server.proxy &

run-create: factory.proxy
	./Create "$$(cat server.proxy)" > obj.proxy

run-monitor: Monitor obj.proxy
	@echo Keep this console open
	./Monitor --Ice.Config=monitor.cfg "$$(cat obj.proxy)"

run-modify: Modify
	./Modify "$$(cat obj.proxy)" true
	./Modify "$$(cat obj.proxy)" false
