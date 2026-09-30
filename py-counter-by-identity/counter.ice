// Interface definition of the Counter service. Run `slice2py counter.ice` to
// generate the client proxy and the server skeleton.

module Example {
    interface Counter {
        long increment();
        idempotent long get();
    };
};
