Description
===========

This example describes a distributed application with IceGrid that runs two Printer servers implemented in Python (`py/hello` directory) on two nodes (node1 and node2). There is no file deployment: the servers run the programs directly from the `py/hello` directory of this repository. The application includes the definition of a "well-known" object called "printer1" for the Printer object of the server that runs on node1.

In a real production system, it would be normal to run a single IceGrid Node on each computer involved. Here, for simplicity, we run the two IceGrid nodes that we are going to use on the user's computer.

Here is the usage and meaning of the different files:

- `Makefile`: Has targets to start and stop the nodes, add the application to the Registry (`load-app`) and run the client.
- `node1.config`: Configuration of the first IceGrid node. Includes a "collocated" Registry, meaning both run in the same process.
- `node2.config`: Configuration of the second IceGrid node.
- `locator.config`: Configuration of the Locator reference, necessary for clients accessing the application objects.
- `printerapp-py.xml`: Distributed application using the Printer implemented in Python (`py/hello` directory).
- `well-known.py`: A Python client that invokes the well-known object "printer1".


Execution
=========

These instructions use the icegridadmin program, but all these steps can also be performed with icegridgui.

Start the nodes (from this directory, since the paths of the programs in the XML file are relative to it):

    $ make start-grid

The output of the nodes, and that of their servers, is shown in this terminal (the `Ice.StdOut` property is empty).

Load the application into the Registry:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application add printerapp-py.xml"

or:

    $ make load-app

PrinterServer1 has on-demand activation: the Registry starts it when a client looks for its adapter. Invoke it with:

    $ ../py/hello/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter"

or:

    $ make run-client

The server prints its proxy and the message in the terminal of the nodes:

    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter
    0: Hello World!

As "printer1" is a well-known object, the client does not need to know its adapter:

    $ ./well-known.py --Ice.Config=locator.config

PrinterServer2 has manual activation, so it must be started explicitly:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer2"

Its proxy (with a UUID as identity) is shown in the terminal of the nodes.

Stop the nodes with:

    $ make stop-grid

or remove their data (`/tmp/icedata`) too with:

    $ make clean
