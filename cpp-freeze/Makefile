#!/usr/bin/make -f

include ../cpp-common.mk

CXXFLAGS += -I$(ICE_HOME)/include
LDFLAGS=-L$(ICE_HOME)/lib
LDLIBS=-lIce -lIceUtil -lstdc++ -lpthread -lrt

SLICE=counter

all: server client

server: LDLIBS+=-lFreeze
server: server.o $(SLICE).o
server.o: server.cpp $(SLICE).h

client: client.o $(SLICE).o
client.o: client.cpp $(SLICE).h

%.h %.cpp: %.ice
	slice2cpp $<

run-server: server db
	./server --Ice.Config=server.cfg | tee server.out

run-client: client
	grep -v "^--" server.out > proxy.out
	./client '$$(head -1 proxy.out)'

db:
	mkdir db

clean:
	$(RM) *~ *.o $(SLICE).h $(SLICE).cpp server client
	$(RM) db/* server.out proxy.out
