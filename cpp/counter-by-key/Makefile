#!/usr/bin/make -f

include ../common.mk

SLICE=counter
STUBS=$(addprefix $(SLICE), .h .cpp)
TARGET=server client

all: $(TARGET)

server: server.o $(SLICE).o
client: client.o $(SLICE).o

server.cpp client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) $(TARGET) $(STUBS) *.o *~ proxy.out

run-server: server
	./server --Ice.Config=server.config | tee proxy.out

run-client: client
	./client '$(shell head -1 proxy.out)'
