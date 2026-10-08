Description
===========

This example describes a distributed application with IceGrid that runs two Printer servers implemented in C++ (`cpp/hello` directory) on two nodes (node1 and node2). There is an equivalent example for every language in `cpp/icegrid`, `java/icegrid` and `py/icegrid`.

In a real production system, it would be normal to run a single IceGrid Node on each computer involved. Here, for simplicity, we run the two IceGrid nodes that we are going to use on the user's computer.

Here is the usage and meaning of the different files:

- `Makefile`: Has targets to start and stop the nodes, add the application to the Registry (`load-app`), deploy the programs with Ansible (`deploy`) and run the client.
- `node1.config`: Configuration of the first IceGrid node. Includes a "collocated" Registry, meaning both run in the same process.
- `node2.config`: Configuration of the second IceGrid node.
- `locator.config`: Configuration of the Locator reference, necessary for clients accessing the application objects.
- `inventory.ini`: Ansible inventory, with a host for each IceGrid node.
- `group_vars/all.yml`: Variables for the playbook: the `icegridadmin` command and the servers to stop.
- `deploy.yml`: Ansible playbook that distributes the programs to the nodes.
- `printerapp.xml`: Distributed application using the Printer implemented in C++ (`cpp/hello` directory).


Execution
=========

These instructions use the icegridadmin program, but all these steps can also be performed with icegridgui.

Start the nodes:

    $ make start-grid

Load the application into the Registry:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "application add printerapp.xml"

File distribution. The servers run the programs found in `/tmp/printer-cpp/<node>` on each node (see the `exe` and `pwd` attributes in the XML file). First, `make gen-dist` in the example directory (`cpp/hello`) builds the programs and puts the files to deploy in its `dist` directory. Then the Ansible playbook `deploy.yml` disables and stops the servers, copies the `dist` directory to every node and enables the servers again:

    $ make -C ../hello gen-dist
    $ ansible-playbook -i inventory.ini deploy.yml

`make deploy` runs the playbook (it does not run `make gen-dist`).

In this example every node runs on the local computer (`ansible_connection=local` in `inventory.ini`). For a real deployment, set `ansible_host` for each node to the address of its computer.

Start the servers (since they have manual activation):

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer1"
    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server start PrinterServer2"

You can see the server output (where the object proxy appears) with:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter

Finally, you can invoke the PrinterServer1 server with:

    $ ../hello/client --Ice.Config=locator.config "printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter"

And verify that it has been executed by checking the server output again:

    $ icegridadmin --Ice.Config=locator.config -u user -p pass -e "server show PrinterServer1 stdout"
    server `PrinterServer1' stdout:
    printer1 -t -e 1.1 @ PrinterServer1.PrinterAdapter
    Hello World!
