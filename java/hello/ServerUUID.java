import com.zeroc.Ice.Object;
import com.zeroc.Ice.*;

public class ServerUUID extends Application {
    public int run(String[] args) {
        Object servant = new PrinterI();

        ObjectAdapter adapter =
            communicator().createObjectAdapter("PrinterAdapter");
        ObjectPrx proxy = adapter.addWithUUID(servant);

        System.out.println(communicator().proxyToString(proxy));

        adapter.activate();
        shutdownOnInterrupt();
        communicator().waitForShutdown();

        return 0;
    }

    static public void main(String[] args) {
        ServerUUID app = new ServerUUID();
        app.main("ServerUUID", args);
    }
}
