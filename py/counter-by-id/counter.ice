module Example {
    interface Counter {
        long increment();
        idempotent long get();
    };
};
