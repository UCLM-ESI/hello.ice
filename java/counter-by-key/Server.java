import java.util.HashMap;
import java.util.Map;

import com.zeroc.Ice.*;

class CounterI implements Example.Counter {
    private final Map<String, Long> counters = new HashMap<>();

    @Override
    public void create(String name, Current current) {
        System.err.println("Received request to create counter: " + name);
        if (counters.containsKey(name)) {
            System.err.println("Counter " + name + " already exists");
            return;
        }

        counters.put(name, 0L);
    }

    @Override
    public void increment(String name, long delta, Current current)
            throws Example.NotFound {
        System.err.println("Received request to increment " + name + " by " + delta);
        if (!counters.containsKey(name))
            throw new Example.NotFound(name);

        counters.put(name, counters.get(name) + delta);
    }

    @Override
    public long get(String name, Current current) throws Example.NotFound {
        System.err.println("Received request to get counter: " + name);
        if (!counters.containsKey(name))
            throw new Example.NotFound(name);

        return counters.get(name);
    }

    @Override
    public Map<String, Long> list(Current current) {
        System.err.println("Received request to list counters");
        return new HashMap<>(counters);
    }
}

public class Server extends Application {
    public int run(String[] args) {
        ObjectAdapter adapter =
            communicator().createObjectAdapter("CounterAdapter");

        ObjectPrx proxy = adapter.add(new CounterI(), Util.stringToIdentity("counter"));

        System.out.println(communicator().proxyToString(proxy));

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
