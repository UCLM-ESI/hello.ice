CC=g++
CXXFLAGS=-I.
LDLIBS=-lIce -lIceUtil

SLICE=factorial
STUBS=$(addprefix $(SLICE), .h .cpp)

all: Server Client

Server: Server.o $(SLICE)I.o $(SLICE).o WorkQueue.o
Client: Client.o $(SLICE).o

Server.cpp Client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) Server Client *.o server.proxy
	$(RM) $(STUBS) *~
	$(RM) *.bz2 IcePatch2.sum

run-server: Server
	./Server --Ice.Config=./hello.cfg | tee server.proxy

run-client: Client
	./Client "$(shell head -1 server.proxy)" 4
