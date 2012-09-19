include ../vars.mk

CXXFLAGS = -I.
LDLIBS = -lIce -lIceUtil -lIceStorm

APP=Hello
STUBS=$(addprefix $(APP), .h .cpp)

all: publisher subscriber

publisher: publisher.o $(APP).o
subscriber: subscriber.o $(APP).o

publisher.cpp subscriber.cpp: $(STUBS)

%.h %.cpp: %.ice
	slice2cpp $<

clean:
	$(RM) publisher subscriber *.o *~
	$(RM) -r db $(STUBS)


run-subscriber: subscriber
	./subscriber --Ice.Config=subscriber.config

run-publisher: publisher
	./publisher --Ice.Config=publisher.config

start: /usr/bin/icebox /usr/bin/icestormadmin
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	sleep 3
	icestormadmin --Ice.Config=icestorm.config -e "create HelloTopic"

stop:
	icestormadmin --Ice.Config=icestorm.config -e "destroy HelloTopic"
	killall icebox
