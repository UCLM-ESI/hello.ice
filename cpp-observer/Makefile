#!/usr/bin/make -f

include ../cpp-common.mk

LDLIBS += -lIceStorm

SLICES=$(wildcard *.ice)
GENERATED=$(SLICES:.ice=.cpp) $(SLICES:.ice=.h)
TARGET=server Create Modify Monitor

all: $(TARGET)

server: server.o Bool.o BoolObservable.o BoolFactory.o
server.o: server.cpp Bool.h BoolObservable.h BoolFactory.h

Create: Create.o BoolFactory.o
Create.o: Create.cpp BoolFactory.h

Modify: Modify.o Bool.o
Modify.o: Modify.cpp Bool.h

Monitor: Monitor.o Bool.o BoolObservable.o
Monitor.o: Monitor.cpp BoolObservable.h Bool.h

BoolObservable.h BoolObservable.cpp: Bool.ice

%.h %.cpp: %.ice
	slice2cpp -I/usr/share/ice/slice $<

clean:
	$(RM) $(TARGET)
	$(RM) *.o *~ $(GENERATED)
	$(RM) server.proxy obj.proxy

start: /usr/bin/icebox
	icebox --Ice.Config=icebox.config &

stop:
	-killall icebox
	-killall server

run-server: server
	./server --Ice.Config=server.cfg | tee server.proxy

run-create: Create
	./Create "$$(head -1 server.proxy)" | tee obj.proxy

run-monitor: Monitor
	@echo Keep this console open
	./Monitor --Ice.Config=monitor.cfg "$$(cat obj.proxy)"

run-modify: Modify
	./Modify "$$(cat obj.proxy)" true
	./Modify "$$(cat obj.proxy)" false
