#!/usr/bin/make -f

include ../common.mk

LDLIBS += -lIceStorm

SLICES=$(wildcard *.ice)
GENERATED=$(SLICES:.ice=.cpp) $(SLICES:.ice=.h)
TARGET=server create modify monitor

all: $(TARGET)

server: server.o Bool.o BoolObservable.o BoolFactory.o
server.o: server.cpp Bool.h BoolObservable.h BoolFactory.h

create: create.o BoolFactory.o
create.o: create.cpp BoolFactory.h

modify: modify.o Bool.o
modify.o: modify.cpp Bool.h

monitor: monitor.o Bool.o BoolObservable.o
monitor.o: monitor.cpp BoolObservable.h Bool.h

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

run-create: create
	./create "$$(head -1 server.proxy)" | tee obj.proxy

run-monitor: monitor
	@echo Keep this console open
	./monitor --Ice.Config=monitor.cfg "$$(cat obj.proxy)"

run-modify: modify
	./modify "$$(cat obj.proxy)" true
	./modify "$$(cat obj.proxy)" false
