#!/usr/bin/make -f

include ../cpp-common.mk

# APP=Callback Printer
# STUBS=$(addprefix $(APP), .h .cpp)
TARGET=server client

all: $(TARGET)

server: server.o callbackI.o callback.o printer.o
# server-uuid: server-uuid.o $(APP)I.o $(APP).o
client: client.o callback.o printer.o printerI.o

server.cpp client.cpp: callback.h callback.cpp printer.h printer.cpp

%.cpp %.h: %.ice
	slice2cpp -I/usr/share/Ice-3.6.1/slice $<

dist:
	mkdir dist

gen-dist: all dist
	cp client server dist/
	icepatch2calc dist/

clean:
	$(RM) $(TARGET) callback.h callback.cpp printer.h printer.cpp *.o *~
	$(RM) *.bz2 IcePatch2.sum
	$(RM) -r dist

calc:
	icepatch2calc .

run-server: server
	./server --Ice.Config=server.config | tee proxy.out

run-client: client
	./client '$(shell head -1 proxy.out)'
