include ../vars.mk

CXXFLAGS=-I.
LDLIBS=-lIce -lIceUtil

APP=Hello
STUBS=$(addprefix $(APP), .h .cpp)

all: Server Client

Server: Server.o $(APP)I.o $(APP).o
Client: Client.o $(APP).o

Server.cpp Client.cpp: $(STUBS)

%.cpp %.h: %.ice
	slice2cpp $<

clean:
	$(RM) Server Client $(STUBS) *.o *~
	$(RM) *.bz2 IcePatch2.sum
