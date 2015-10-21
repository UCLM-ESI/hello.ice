# -*- mode:makefile -*-

all: Server.exe Client.exe
Server.exe: Server.cs Printer.cs
Client.exe: Client.cs Printer.cs

%.exe: %.cs
	mono-csc -out:$@ -pkg:Ice-3.5 $^

%.cs: %.ice
	slice2cs $<

clean:
	$(RM) *~ *.exe proxy.out Printer.cs

run-server: Server.exe
	mono Server.exe --Ice.Config=Server.config | tee proxy.out

run-client: Client.exe
	mono Client.exe '$(shell head -1 proxy.out)'
