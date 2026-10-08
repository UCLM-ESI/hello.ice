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

gen-dist: all
	$(RM) -r dist
	mkdir dist
	cp server server-uuid dist/

clean:
	$(RM) $(TARGET) $(STUBS) *.o *~
	$(RM) -r dist

run-server: server
	./server --Ice.Config=server.config | tee proxy.out

run-client: client
	./client '$(shell head -1 proxy.out)'
