#!/usr/bin/make -f
# -*- mode:makefile -*-

clean:
	$(RM) *~ proxy.out

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'
