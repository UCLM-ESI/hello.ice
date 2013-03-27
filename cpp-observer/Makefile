CXX=g++-4.6
LDLIBS=-lIce -lIceUtil -lFreeze -lIceStorm
CXXFLAGS=-I.

SLICES=$(wildcard *.ice)
GENERATED=$(SLICES:.ice=.cpp) $(SLICES:.ice=.h)

# NWSRC=\
#	Bool.ice \
#	BoolPersistent.ice \
#	BoolFactory.ice \
#	Server.cpp \
#	Client.cpp \
#	Create.cpp \
#	Modify.cpp \
#	Monitor.cpp

all: Server Create Modify Monitor

Server: Server.o Bool.o BoolPersistent.o BoolFactory.o
Server.o: Server.cpp Bool.h BoolPersistent.h BoolFactory.h

Create: Create.o BoolFactory.o
Create.o: Create.cpp BoolFactory.h

Modify: Modify.o Bool.o
Modify.o: Modify.cpp Bool.h

Monitor: Monitor.o Bool.o BoolPersistent.o
Monitor.o: Monitor.cpp BoolPersistent.h Bool.h

clean:
	$(RM) *.o *~ Client Server $(GENERATED)
	$(RM) Create Modify Monitor
	$(RM) -rf bin

%.h %.cpp: %.ice
	slice2cpp -I/usr/share/Ice/slice $<
