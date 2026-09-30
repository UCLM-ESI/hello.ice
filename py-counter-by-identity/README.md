# Counter: one remote object per counter

A counter service in which **each counter is a remote object of its own**,
addressed by its identity: `counter1` and `counter2` keep independent counts
although they share server, adapter and interface.

Compare it with [`../py-counter-by-key`](../py-counter-by-key), which solves
the same problem the other way round: a single remote object holding a
dictionary, with the counter to act on passed as an argument
(`increment(name, delta)`). That is how it has to be done with plain RPC, where
the server offers a flat set of procedures and nothing distinguishes one
entity from another. Here the identity does the distinguishing, which is what
the object model buys.

## Depends

- `zeroc-ice-compilers` (slice2py)
- `python3-zeroc-ice`

## Files

- `counter.ice` -- the interface in Slice. `get` is declared `idempotent`, so
  the runtime is allowed to retry it; `increment` is not.
- `server.config` -- the adapter endpoint, as an Ice property.
- `server.py`, `client.py` -- the programmer's code. `CounterI` implements the
  generated skeleton; every operation takes an extra `Ice::Current` argument.

Unlike most examples here, the stubs come from `slice2py` (see the Makefile)
rather than from `Ice.loadSlice`, so that the compilation step is visible.

## Try it

```
$ make
$ ./server.py --Ice.Config=server.config &
counter1 -t -e 1.1:tcp -h localhost -p 2002 -t 60000
counter2 -t -e 1.1:tcp -h localhost -p 2002 -t 60000
$ ./client.py 'counter1 -t:tcp -h localhost -p 2002'
$ ./client.py 'counter2 -t:tcp -h localhost -p 2002'
```

The proxy the server prints is the whole remote object reference: identity,
invocation mode (`-t`, twoway), encoding version and the list of endpoints.
