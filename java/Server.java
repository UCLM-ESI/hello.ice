import Ice.*;

public class Server extends Ice.Application {
    public int run(String[] args) {
	Ice.Object servant = new HelloI();

	ObjectAdapter adapter =
	    communicator().createObjectAdapter("HelloAdapter");
	ObjectPrx proxy = 
	    adapter.add(servant, Util.stringToIdentity("hello1"));

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
