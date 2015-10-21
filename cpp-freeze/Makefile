#!/usr/bin/make -f
# -*- mode:makefile -*-

include ../cpp-common.mk

CXXFLAGS += -I$(ICE_HOME)/include
LDFLAGS=-L$(ICE_HOME)/lib
LDLIBS=-lIce -lIceUtil -lstdc++ -lpthread -lrt

SLICE=counter

all: Server Client

Server: LDLIBS+=-lFreeze
Server: Server.o $(SLICE).o
Server.o: Server.cpp $(SLICE).h

Client: Client.o $(SLICE).o
Client.o: Client.cpp $(SLICE).h

%.h %.cpp: %.ice
	slice2cpp $<

run-server: Server db
	./Server --Ice.Config=server.cfg | tee server.out

run-client: Client
	grep -v "^--" server.out > proxy.out
	./Client '$$(head -1 proxy.out)'

db:
	mkdir db

clean:
	$(RM) *~ *.o $(SLICE).h $(SLICE).cpp Server Client
	$(RM) db/* server.out proxy.out
