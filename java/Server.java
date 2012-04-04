import Ice.*;

public class Server extends Ice.Application {
    public int run(String[] args) {
	ObjectAdapter oa = communicator().createObjectAdapter("HelloAdapter");
	ObjectPrx prx = oa.add(new HelloI(), Util.stringToIdentity("hello1"));
	oa.activate();

	System.out.println(communicator().proxyToString(prx));

	shutdownOnInterrupt();
	communicator().waitForShutdown();

	return 0;
    }

    static public void main(String[] args) {
	Server app = new Server();
	app.main("Server", args);
    }
}
