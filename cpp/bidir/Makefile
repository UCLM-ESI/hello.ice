#!/usr/bin/make -f

include ../common.mk

# APP=Callback Printer
# STUBS=$(addprefix $(APP), .h .cpp)
TARGET=server client

all: $(TARGET)

server: server.o callbackI.o callback.o printer.o
# server-uuid: server-uuid.o $(APP)I.o $(APP).o
client: client.o callback.o printer.o printerI.o

server.cpp client.cpp: callback.h callback.cpp printer.h printer.cpp

%.cpp %.h: %.ice
	slice2cpp -I/usr/share/ice/slice $<

gen-dist: all
	$(RM) -r dist
	mkdir dist
	cp client server dist/

clean:
	$(RM) $(TARGET) callback.h callback.cpp printer.h printer.cpp *.o *~
	$(RM) -r dist

run-server: server
	./server --Ice.Config=server.config | tee proxy.out

run-client: client
	./client '$(shell head -1 proxy.out)'
