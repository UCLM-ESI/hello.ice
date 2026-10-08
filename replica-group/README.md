# IceGrid Replica Group

Two IceGrid nodes (docker containers) run a ToolServer each ([../py/upper](../py/upper)). Both adapters belong to the replica group `ToolGroup`, and the client uses the indirect proxy `tool1 @ ToolGroup`. Each XML file is the same application with a different load balancing policy.

    $ make up
    $ make round-robin      # or: random, ordered, adaptive
    $ make round-client
    HELLO WORLD!

`make logs` shows which server got each invocation:

- **round-robin**: alternates between ToolServer1 and ToolServer2.
- **random**: a random replica each time.
- **ordered**: the adapter with the lowest `priority` (ToolServer1) while it is available.
- **adaptive**: the least loaded node (load average of the last 5 minutes). As both containers run on the same host, they report the same load.
