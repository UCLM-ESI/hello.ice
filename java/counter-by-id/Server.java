import com.zeroc.Ice.*;

class CounterI implements Example.Counter {
    private long value = 0;

    @Override
    public long increment(Current current) {
        return ++value;
    }

    @Override
    public long get(Current current) {
        return value;
    }
}

public class Server extends Application {
    public int run(String[] args) {
        ObjectAdapter adapter =
            communicator().createObjectAdapter("CounterAdapter");

        ObjectPrx proxy1 = adapter.add(new CounterI(), Util.stringToIdentity("counter1"));
        ObjectPrx proxy2 = adapter.add(new CounterI(), Util.stringToIdentity("counter2"));

        System.out.println(communicator().proxyToString(proxy1));
        System.out.println(communicator().proxyToString(proxy2));

        adapter.activate();
        shutdownOnInterrupt();
        communicator().waitForShutdown();

        return 0;
    }

    static public void main(String[] args) {
        Server app = new Server();
        app.main("Server", args);
    }
}
