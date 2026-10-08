Description
===========

This example illustrates a realistic deployment of an IceGrid application on several remote nodes. Ansible logs into each node by SSH and copies to it the Printer server implemented in Python (`py/hello` directory). Here the remote nodes are two Docker containers, each one with its own address, but the procedure is the same with real computers: only their addresses in `inventory.ini` would change. Unlike `icegrid-docker`, the nodes do not mount the program from the host.

Every component runs in its own Docker container with a fixed address:

- `registry` (172.29.0.10): IceGrid Registry.
- `node1` (172.29.0.11) and `node2` (172.29.0.12): IceGrid nodes. Besides `icegridnode`, they run an SSH server, so that Ansible can log in as `ice`, the user that runs the node and its servers.
- `loader`: adds the application (`app.xml`) to the Registry and exits.

Files:

- `compose.yml`: Docker services.
- `../docker/ignode`: image for the nodes, shared by all the examples that run in Docker: the ZeroC IceGrid node image plus Ice for Python and the SSH server, that starts when a public key is mounted in `/run/authorized_key.pub` (see `compose.yml`).
- `registry.config`, `node1.config`, `node2.config`: configuration of the Registry and the nodes.
- `locator.config`: Locator reference, used by the client and `icegridadmin` on the host.
- `app.xml`: the application: a Printer server (`./server.py`) on each node, running in `/var/lib/ice/printer`.
- `inventory.ini`: Ansible inventory, with the address of each node and the SSH settings.
- `group_vars/all.yml`: variables for the playbook: the `icegridadmin` command and the servers to stop.
- `deploy.yml`: Ansible playbook that copies the programs to the nodes.
- `Makefile`: targets to run every step.


Execution
=========

Start the Registry and the nodes. It also generates an SSH key pair (in `ssh/`, ignored by git) whose public key is accepted by the nodes, and loads the application:

    $ make start-grid

Prepare the files to deploy (the `dist` directory of `py/hello`):

    $ make -C ../py/hello gen-dist

Deploy them. The playbook disables and stops the servers, copies `py/hello/dist` to `/var/lib/ice/printer` in every node by SSH and enables the servers again:

    $ make deploy

Start the servers (they have manual activation) and invoke both of them:

    $ make start-servers
    $ make run-client

Check the output of the servers:

    $ make show-server-out

Other targets: `show-nodes`, `show-logs` (output of the containers), `load-app` (load `app.xml` again after changing it), `stop-grid` and `clean` (it also removes the SSH keys).

Note that the containers are created again by `make start-grid` after `make stop-grid`, so you have to deploy the programs again.
