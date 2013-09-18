LDLIBS=-lIce -lFreeze -lIceUtil -pthread
CXXFLAGS=-I.
CC=$(CXX)

all: listin

listin: listin.o Listin.o ListinMap.o
listin.o: listin.cpp Listin.h ListinMap.h

%.h %.cpp: %.ice
	slice2cpp $<

ListinMap.h ListinMap.cpp: Listin.ice
	slice2freeze --dict ListinMap,string,Listin::Registro --dict-index ListinMap,telefono ListinMap $<

clean:
	$(RM) *.o *~ listin ListinMap.h ListinMap.cpp Listin.h Listin.cpp
	$(RM) -r db/*
