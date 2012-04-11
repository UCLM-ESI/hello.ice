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
            Ice.Identity identity = Ice.Util.stringToIdentity("counter" + i);
            if (!evictor.hasObject(identity)) {
                ObjectPrx proxy = evictor.add(new CounterI(), identity);
                System.out.println(communicator().proxyToString(proxy));
	    }
	}

	adapter.addServantLocator(evictor, "");
	adapter.activate();

	System.out.println("Ready");
	communicator().waitForShutdown();
	System.out.println("Done");
	return 0;
    }

    public static void main (String[] args) {
	Server app = new Server();
	System.exit(app.main("Server", args));
    }
}
