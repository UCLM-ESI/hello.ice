include ../common.mk

CXXFLAGS=-I.

APP=Printer
STUBS=$(addprefix $(APP), .h .cpp)

all: Server Client

Server: Server.o $(APP)I.o $(APP).o
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
	$(RM) Server Client $(STUBS) *.o *~
	$(RM) *.bz2 IcePatch2.sum
	$(RM) -r dist

calc:
	icepatch2calc .

run-server: Server
	./Server --Ice.Config=Server.config | tee proxy.out

run-client: Client
	./Client "$(shell head -1 proxy.out)"
