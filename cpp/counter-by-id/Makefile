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
	$(RM) $(TARGET) $(STUBS) *.o *~

run-server: server
	./server --Ice.Config=server.config

run-client: client
	./client 'counter1 -t:tcp -h localhost -p 2002'
