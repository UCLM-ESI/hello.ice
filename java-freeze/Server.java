import Ice.*;

public class Server extends Ice.Application {
    public int run (String[] args) {
	shutdownOnInterrupt();

        communicator().addObjectFactory(
            new CounterFactory(),
	    Counter.RWPersistent.ice_staticId());

	adapter = communicator().createObjectAdapter("PrinterAdapter");
        evictor = Freeze.Util.createBackgroundSaveEvictor(
            adapter, "db", "counters",
	    new CounterInitializer(), null, true);

	for (int i=0; i<5; ++i) {
	    ObjectPrx proxy = create_or_get_counter("counter" + i);
	    System.out.println(communicator().proxyToString(proxy));
	}

	adapter.addServantLocator(evictor, "");
	adapter.activate();

	System.out.println("-- Ready");
	communicator().waitForShutdown();
	System.out.println("-- Done");
	return 0;
    }

    ObjectPrx create_or_get_counter(String identity_str) {
	Identity identity = Ice.Util.stringToIdentity(identity_str);

	if (evictor.hasObject(identity))
	    return adapter.createProxy(identity);

	System.out.println("-- New counter " + identity_str);
	return evictor.add(new CounterI(), identity);
    }

    public static void main (String[] args) {
	Server app = new Server();
	System.exit(app.main("Server", args));
    }

    private ObjectAdapter adapter;
    private Freeze.Evictor evictor;
}
