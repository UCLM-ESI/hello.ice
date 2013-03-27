CXX=g++-4.6
CXXFLAGS=-I.
LDLIBS=-lIce -lIceUtil

SLICE=Hello
STUBS=$(addprefix $(SLICE), .h .cpp)

all: Server Client

Server: Server.o $(SLICE)I.o $(SLICE).o
Client: Client.o $(SLICE).o

Server.cpp Client.cpp: $(STUBS)

vpath %.ice ../

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) Server Client *.o
	$(RM) $(STUBS) *~
