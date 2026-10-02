#

STUBS = counter_ice.py Example

all: $(STUBS)

counter_ice.py Example: counter.ice
	slice2py counter.ice

run-server: all
	./server.py --Ice.Config=server.config

run-client: all
	./client.py 'counter1 -t:tcp -h localhost -p 2002'

clean:
	$(RM) *~ counter_ice.py
	$(RM) -r Example __pycache__
