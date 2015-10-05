import Ice.*;

public class Server extends Ice.Application {
    public int run(String[] args) {
        Ice.Object servant = new PrinterI();

        ObjectAdapter adapter =
	       communicator().createObjectAdapter("PrinterAdapter");
	   ObjectPrx proxy =
	       adapter.add(servant, Util.stringToIdentity("printer1"));

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
