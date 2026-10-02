import com.zeroc.Ice.*;

public class Client extends Application {
    public int run(String[] args) {
        ObjectPrx proxy = communicator().stringToProxy(args[0]);
        Example.CounterPrx counter = Example.CounterPrx.checkedCast(proxy);

        if (counter == null)
            throw new RuntimeException("invalid proxy");

        try {
            counter.create("counter1");
            counter.increment("counter1", 5);
            System.out.println("After incrementing counter1 by 5: " + counter.get("counter1"));
        } catch (Example.NotFound e) {
            System.err.println("Counter not found: " + e.name);
            return 1;
        }

        return 0;
    }

    static public void main(String[] args) {
        Client app = new Client();
        app.main("Client", args);
    }
}
