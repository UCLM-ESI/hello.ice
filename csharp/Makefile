
all: server.exe client.exe
server.exe: server.cs printer.cs
client.exe: client.cs printer.cs

%.exe: %.cs
	mono-csc -out:$@ -pkg:Ice-3.5 $^

%.cs: %.ice
	slice2cs $<

clean:
	$(RM) *~ *.exe proxy.out printer.cs

run-server: server.exe
	mono server.exe --Ice.Config=server.config | tee proxy.out

run-client: client.exe
	mono client.exe '$(shell head -1 proxy.out)'
