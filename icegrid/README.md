Description
===========

This example describes a distributed application with IceGrid that deploys two Printer servers on two nodes (node1 and node2).

In a real production deployment, it would be normal to run a single IceGrid Node on each computer involved. Here, for simplicity, we run the two IceGrid nodes that we are going to use on the user's computer.

Here is the usage and meaning of the different files:

- `Makefile`: Has targets to start and stop the nodes, deploy and distribute the application and run the client.
- `node1.config`: Configuration of the first IceGrid node. Includes a "collocated" Registry, meaning both run in the same process.
- `node2.config`: Configuration of the second IceGrid node.
- `locator.config`: Configuration of the Locator reference, necessary for clients accessing the deployed objects.
- `inventory.ini`: Ansible inventory, with a host for each IceGrid node.
- `group_vars/all.yml`: Variables for the playbook: the `icegridadmin` command and the servers to stop.
- `deploy.yml`: Ansible playbook that distributes the programs to the nodes.
- `printerapp-cpp.xml`: Distributed application using the Printer implemented in C++ (hello.ice/cpp/hello directory).
- `printerapp-java.xml`: Distributed application using the Printer implemented in Java (hello.ice/java/hello directory).
- `printerapp-py.xml`: Distributed application using the Printer implemented in Python (hello.ice/py/hello directory).
- `query-client.py`: Example usage of the IceGrid::Query interface for object search (requires adding "printer1" as a well-known object, see the exercises in the book).


Execution
=========

These instructions use the icegridadmin program, but all these steps can also be performed with icegridgui.

Start the nodes:

    $ make start-grid

Load the application into the Registry:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application add printerapp-py.xml"

File distribution. The servers run the programs found in `/tmp/printer-py/<node>` on each node (see the `exe` and `pwd` attributes in the XML file). The Ansible playbook `deploy.yml` runs `make gen-dist` in the example directory (e.g. `py/hello`), which builds the programs and puts the files to deploy in its `dist` directory. Then it disables and stops the servers, copies the `dist` directory to every node and enables the servers again:

    $ ansible-playbook -i inventory.ini deploy.yml

Use `-e lang=cpp` or `-e lang=java` to deploy the C++ or Java version (along with `printerapp-cpp.xml` or `printerapp-java.xml`). In this example every node runs on the local computer (`ansible_connection=local` in `inventory.ini`). For a real deployment, set `ansible_host` for each node to the address of its computer.

Start the servers (since they have manual activation):

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer1"
    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer2"

You can see the server output (where the object proxy appears) with:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter

Finally, you can invoke the PrinterServer1 server with:

    $ ../py/hello/client.py --Ice.Config=locator.config "printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter"

And verify that it has been executed by checking the server output again:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter
    0: Hello World!
