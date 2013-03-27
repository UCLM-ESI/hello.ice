
CC=g++
CXX=g++-4.6
CXXFLAGS = -I.
LDLIBS = -lIce -lIceUtil -lIceStorm

SLICE = Hello
STUBS=$(addprefix $(SLICE), .h .cpp)

all: publisher subscriber

publisher: publisher.o $(SLICE).o
subscriber: subscriber.o $(SLICE).o

publisher.cpp subscriber.cpp: $(STUBS)

vpath %.ice ../

%.h %.cpp: %.ice
	slice2cpp $<

clean:
	$(RM) publisher subscriber *.o *~
	$(RM) -r db $(STUBS)


run-subscriber: subscriber
	./subscriber --Ice.Config=icestorm.config

run-publisher: publisher
	./publisher --Ice.Config=icestorm.config

start: /usr/bin/icebox /usr/bin/icestormadmin
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	sleep 3
	icestormadmin --Ice.Config=icestorm.config -e "create HelloTopic"

stop:
	icestormadmin --Ice.Config=icestorm.config -e "destroy HelloTopic"
	killall icebox
