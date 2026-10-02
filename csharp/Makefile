#!/usr/bin/make -f

all: bin/server.dll bin/client.dll

bin/%.dll: %.csproj %.cs printer.cs
	dotnet build $< -o bin

printer.cs: printer.ice
	slice2cs $<

clean:
	$(RM) *~ proxy.out printer.cs
	$(RM) -r bin obj

run-server: bin/server.dll
	dotnet bin/server.dll --Ice.Config=server.config | tee proxy.out

run-client: bin/client.dll
	dotnet bin/client.dll '$(shell head -1 proxy.out)'

docker-run:
	docker compose up --build --abort-on-container-exit --exit-code-from client
	docker compose down

docker-clean:
	docker compose down --rmi all
