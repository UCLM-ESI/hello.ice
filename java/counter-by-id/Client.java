import com.zeroc.Ice.*;

public class Client extends Application {
    public int run(String[] args) {
        ObjectPrx proxy = communicator().stringToProxy(args[0]);
        Example.CounterPrx counter = Example.CounterPrx.checkedCast(proxy);

        if (counter == null)
            throw new RuntimeException("invalid proxy");

        System.out.println("get() = '" + counter.get() + "'");
        System.out.println("increment() = '" + counter.increment() + "'");
        System.out.println("increment() = '" + counter.increment() + "'");
        System.out.println("get() = '" + counter.get() + "'");

        return 0;
    }

    static public void main(String[] args) {
        Client app = new Client();
        app.main("Client", args);
    }
}
