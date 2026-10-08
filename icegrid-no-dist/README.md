Description
===========

This example describes a distributed application with IceGrid that deploys two Printer servers on two nodes (node1 and node2). The application includes the definition of a "well-known" object called "printer1" for the Printer object of the server deployed on node1.

In a real production deployment, it would be normal to run a single IceGrid Node on each computer involved. Here, for simplicity, we run the two IceGrid nodes that we are going to use on the user's computer.

Here is the usage and meaning of the different files:

- `Makefile`: Has targets to start and stop the three nodes.
- `node1.config`: Configuration of the first IceGrid node. Includes a "collocated" Registry, meaning both run in the same process.
- `node2.config`: Configuration of the second IceGrid node.
- `node3.config`: Configuration of the third IceGrid node.
- `locator.config`: Configuration of the Locator reference, necessary for clients accessing the deployed objects.
- `default-templates.xml`: Service templates for creating applications from the Registry.
- `printerapp-cpp.xml`: Distributed application using the Printer implemented in C++ (hello.ice/cpp directory).
- `printerapp-java.xml`: Distributed application using the Printer implemented in Java (hello.ice/java directory).
- `printerapp-py.xml`: Distributed application using the Printer implemented in Python (hello.ice/py directory).
- `well-known.py`: A Python client that invokes the well-known object "printer1".
- `query-client.py`: Example usage of the IceGrid::Query interface for object search.


Execution
=========

These instructions use the icegridadmin program, but all these steps can also be performed with icegridgui.

Start the nodes:

    $ make start-grid

Load the application into the Registry:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application add printerapp-py.xml"

File distribution. The application looks for programs to execute in ${application.distrib}, which is a variable containing the path where the IcePatch2 distribution service will place the files. Therefore, it's necessary to run the distribution first. This requires two steps:

1. Prepare the files. For example, for `hello.ice/py` this can be done with:

    ```bash
    py$ make gen-dist
    ```

    This creates a `py/dist` directory with the files ready for distribution and a link in `/tmp/printer-py`, which facilitates the IcePatch2 configuration.

1. Execute the distribution itself.

    ```bash
    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application patch PrinterApp"
    ```

    You can check all the IcePatch2 configuration details by looking directly at the description in the XML file or loading it with **icegridgui**.

Start the servers (since they have manual activation):

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer1"
    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer2"

You can see the server output (where the object proxy appears) with:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter

Finally, you can invoke the PrinterServer1 server with:

    $ ../py/client.py --Ice.Config=locator.config "printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter"

And verify that it has been executed by checking the server output again:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter
    0: Hello World!
