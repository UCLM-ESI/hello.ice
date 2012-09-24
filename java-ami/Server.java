import Ice.*;

public class Server extends Ice.Application {
    public int run(String[] args) {
	ObjectAdapter adapter = communicator().createObjectAdapter("PrinterAdapter");
	ObjectPrx prx = adapter.add(new MathI(), Util.stringToIdentity("printer1"));

	System.out.println(communicator().proxyToString(prx));

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
