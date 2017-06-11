#!/usr/bin/make -f
# -*- mode:makefile -*-

include ../cpp-common.mk

CC=g++ -std=c++11

APP=Printer
STUBS=$(addprefix $(APP), .h .cpp)
TARGET=Server Server-UUID Client

all: $(TARGET)

Server: Server.o $(APP)I.o $(APP).o
Server-UUID: Server-UUID.o $(APP)I.o $(APP).o
Client: Client.o $(APP).o

Server.cpp Client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

dist:
	mkdir dist

gen-dist: all dist
	cp Client Server dist/
	icepatch2calc dist/

clean:
	$(RM) $(TARGET) $(STUBS) *.o *~
	$(RM) *.bz2 IcePatch2.sum
	$(RM) -r dist

calc:
	icepatch2calc .

run-server: Server
	./Server --Ice.Config=Server.config | tee proxy.out

run-client: Client
	./Client '$(shell head -1 proxy.out)'
