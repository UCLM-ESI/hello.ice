CC=g++
CXXFLAGS=-I. -I$(ICE_HOME)/include
LDFLAGS=-L$(ICE_HOME)/lib
LDLIBS=-lIce -lIceUtil -lstdc++ -lpthread -lrt

all: Server Client

Server: LDLIBS+=-lFreeze
Server: Server.o Hello.o
Server.o: Server.cc Hello.h

Client: Client.o Hello.o
Client.o: Client.cc Hello.h

%.h %.cpp: %.ice
	slice2cpp $<

run-server: Server db
	./Server --Ice.Config=config | tee server.out

run-client: Client
	./Client "$(shell head -1 server.out)"

db:
	mkdir db

clean:
	$(RM) *~ *.o Hello.h Hello.cpp Server Client
	$(RM) db/* server.out
