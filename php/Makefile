#!/usr/bin/make -f

all: printer.php

printer.php: printer.ice
	slice2php $<

run-client: printer.php
	./client.php '$(shell head -1 ../py/proxy.out)'

clean:
	$(RM) *~ printer.php
