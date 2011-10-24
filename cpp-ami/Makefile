CC=g++
CXXFLAGS=-I.
LDLIBS=-lIce -lIceUtil

SLICE=factorial
STUBS=$(addprefix $(SLICE), .h .cpp)

all: Server Client-end

Server: Server.o $(SLICE)I.o $(SLICE).o
Client-end: Client-end.o $(SLICE).o

Server.cpp Client-end.cpp: $(STUBS)

vpath %.ice ../

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) Server Client-end *.o server.proxy
	$(RM) $(STUBS) *~
	$(RM) *.bz2 IcePatch2.sum

run-server:
	./Server --Ice.Config=../hello.cfg | tee server.proxy

run-client:
	./Client "$(shell head -1 server.proxy)" 4
