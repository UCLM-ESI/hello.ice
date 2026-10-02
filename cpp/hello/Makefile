#!/usr/bin/make -f

include ../common.mk

CC=g++ -std=c++11

SLICE=printer
STUBS=$(addprefix $(SLICE), .h .cpp)
TARGET=server server-uuid client

all: $(TARGET)

server: server.o $(SLICE)I.o $(SLICE).o
server-uuid: server-uuid.o $(SLICE)I.o $(SLICE).o
client: client.o $(SLICE).o

server.cpp client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

dist:
	mkdir dist

gen-dist: clean all dist
	cp client server server-uuid dist/
	icepatch2calc dist/
	ln -sf $(CURDIR)/dist /tmp/printer-server-cpp

clean:
	$(RM) $(TARGET) $(STUBS) *.o *~
	$(RM) *.bz2 IcePatch2.sum
	$(RM) -r dist /tmp/printer-server-cpp

calc:
	icepatch2calc .

run-server: server
	./server --Ice.Config=server.config | tee proxy.out

run-client: client
	./client '$(shell head -1 proxy.out)'
