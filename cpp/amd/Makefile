#!/usr/bin/make -f

include ../common.mk

SLICE=factorial
STUBS=$(addprefix $(SLICE), .h .cpp)

all: server client

server: server.o $(SLICE)I.o $(SLICE).o WorkQueue.o
client: client.o $(SLICE).o

server.cpp client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) server client *.o server.proxy
	$(RM) $(STUBS) *~
	$(RM) *.bz2 IcePatch2.sum

run-server: server
	./server --Ice.Config=./server.config | tee server.proxy

run-client: client
	./client '$(shell head -1 server.proxy)' 4
