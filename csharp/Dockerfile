FROM debian:trixie-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates wget make zeroc-ice-compilers && \
    wget -q https://packages.microsoft.com/config/debian/13/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends dotnet-sdk-10.0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_NOLOGO=1

WORKDIR /src
COPY cpp/printer.ice cpp/server.config cpp/
COPY csharp/Makefile csharp/Directory.Build.props \
     csharp/server.csproj csharp/client.csproj \
     csharp/server.cs csharp/client.cs \
     csharp/printer.ice csharp/server.config csharp/

WORKDIR /src/csharp
RUN make
