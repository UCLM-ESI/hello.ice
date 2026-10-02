module Example {
    exception NotFound {string name;}

    dictionary<string, long> CounterDict;

    interface Counter {
        void create(string name);
        void increment(string name, long delta) throws NotFound;
        long get(string name) throws NotFound;
        CounterDict list();
    }
}
