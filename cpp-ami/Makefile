#!/usr/bin/make -f
# -*- mode:makefile -*-

include ../cpp-common.mk

SLICE=factorial
STUBS=$(addprefix $(SLICE), .h .cpp)

all: Server Client-end Client-callback

Server: Server.o $(SLICE)I.o $(SLICE).o
Client-end: Client-end.o $(SLICE).o
Client-callback: Client-callback.o $(SLICE).o

Server.cpp Client-end.cpp Client-callback.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) Server Client-end Client-callback *.o server.proxy
	$(RM) $(STUBS) *~
	$(RM) *.bz2 IcePatch2.sum

run-server:
	./Server --Ice.Config=./Server.config | tee server.proxy

run-client-end:
	./Client-end '$(shell head -1 server.proxy)' 4

run-client-callback:
	./Client-callback '$(shell head -1 server.proxy)' 4
