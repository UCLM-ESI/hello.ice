#!/usr/bin/make -f
# -*- mode:makefile -*-

include ../cpp-common.mk

SLICE=factorial
STUBS=$(addprefix $(SLICE), .h .cpp)

all: Server Client

Server: Server.o $(SLICE)I.o $(SLICE).o WorkQueue.o
Client: Client.o $(SLICE).o

Server.cpp Client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) Server Client *.o server.proxy
	$(RM) $(STUBS) *~
	$(RM) *.bz2 IcePatch2.sum

run-server: Server
	./Server --Ice.Config=./Server.config | tee server.proxy

run-client: Client
	./Client '$(shell head -1 server.proxy)' 4
