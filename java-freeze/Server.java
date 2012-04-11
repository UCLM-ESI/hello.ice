import Ice.*;

public class Server extends Ice.Application {
    public int run (String[] args) {
	shutdownOnInterrupt();

        communicator().addObjectFactory(
            new CounterFactory(),
	    Counter.RWPersistent.ice_staticId());

	ObjectAdapter adapter =
	    communicator().createObjectAdapter("HelloAdapter");

        Freeze.Evictor evictor =
	    Freeze.Util.createBackgroundSaveEvictor(
                adapter, "db", "hello",
		new CounterInitializer(), null, true);

	for (int i=0; i<5; ++i) {
	    String identity_str = "counter" + i;
            Ice.Identity identity = Ice.Util.stringToIdentity(identity_str);
	    ObjectPrx proxy;

            if (!evictor.hasObject(identity)) {
		System.out.println("-- Creating object " + identity_str);
		proxy = evictor.add(new CounterI(), identity);
	    }
	    else {
		proxy = adapter.createProxy(identity);
	    }

	    System.out.println(communicator().proxyToString(proxy));
	}

	adapter.addServantLocator(evictor, "");
	adapter.activate();

	System.out.println("-- Ready");
	communicator().waitForShutdown();
	System.out.println("-- Done");
	return 0;
    }

    public static void main (String[] args) {
	Server app = new Server();
	System.exit(app.main("Server", args));
    }
}
