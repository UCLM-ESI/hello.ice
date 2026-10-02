// Interface definition of the Counter service. Run `slice2cpp counter.ice` to
// generate the client proxy and the server skeleton.

module Example {
    interface Counter {
        long increment();
        idempotent long get();
    };
};
