#!/usr/bin/make -f
# -*- mode:makefile -*-

include ../cpp-common.mk

# APP=Callback Printer
# STUBS=$(addprefix $(APP), .h .cpp)
TARGET=Server Client

all: $(TARGET)

Server: Server.o CallbackI.o Callback.o Printer.o
# Server-UUID: Server-UUID.o $(APP)I.o $(APP).o
Client: Client.o Callback.o Printer.o PrinterI.o

Server.cpp Client.cpp: Callback.h Callback.cpp Printer.h Printer.cpp

%.cpp %.h: %.ice
	slice2cpp -I/usr/share/Ice-3.6.1/slice $<

dist:
	mkdir dist

gen-dist: all dist
	cp Client Server dist/
	icepatch2calc dist/

clean:
	$(RM) $(TARGET) Callback.h Callback.cpp Printer.h Printer.cpp *.o *~
	$(RM) *.bz2 IcePatch2.sum
	$(RM) -r dist

calc:
	icepatch2calc .

run-server: Server
	./Server --Ice.Config=Server.config | tee proxy.out

run-client: Client
	./Client '$(shell head -1 proxy.out)'
