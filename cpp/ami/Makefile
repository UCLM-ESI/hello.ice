#!/usr/bin/make -f

include ../common.mk

SLICE=factorial
STUBS=$(addprefix $(SLICE), .h .cpp)

all: server client-end client-callback

server: server.o $(SLICE)I.o $(SLICE).o
client-end: client-end.o $(SLICE).o
client-callback: client-callback.o $(SLICE).o

server.cpp client-end.cpp client-callback.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) server client-end client-callback *.o server.proxy
	$(RM) $(STUBS) *~
	$(RM) *.bz2 IcePatch2.sum

run-server:
	./server --Ice.Config=./server.config | tee server.proxy

run-client-end:
	./client-end '$(shell head -1 server.proxy)' 4

run-client-callback:
	./client-callback '$(shell head -1 server.proxy)' 4
