# Replicated IceGrid Registry

This example runs two replicas of IceGrid Registry and one IceGrid Node as docker containers. To test the failover system, first start it with:

    $ make up

You can view the service logs with:

    $ make logs
    registry2  | starting icegridregistry...
    registry2  | -- 12/14/25 10:19:16.666 icegridregistry: Node: node `node1' up
    registry2  | -- 12/14/25 10:19:16.678 icegridregistry: Replica: established session with master replica
    node1      | starting icegridnode...
    node1      | -- 12/14/25 10:19:16.645 icegridnode: Replica: established session with replica `Master'
    node1      | node1 ready
    node1      | -- 12/14/25 10:19:16.677 icegridnode: Replica: established session with replica `Slave1'
    registry1  | starting icegridregistry...
    registry1  | -- 12/14/25 10:19:16.642 icegridregistry: Node: node `node1' up
    registry1  | -- 12/14/25 10:19:16.665 icegridregistry: Replica: replica `Slave1' up

Deploy the application with:

    $ make app-deploy

Run the client with:

    $ make run-client
    ../py-upper/client.py --Ice.Config=locator.config "tool1 @ ToolServer1.ToolAdapter"
    HELLO WORLD!

Now you can stop the registry1 container (Master):

    $ $ docker compose stop registry1
    [+] Stopping 1/1
    ✔ Container registry1 Stopped

And verify that the client continues working:

    $ make run-client
    ../py-upper/client.py --Ice.Config=locator.config "tool1 @ ToolServer1.ToolAdapter"
    HELLO WORLD!
