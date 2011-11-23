
public class Server extends Ice.Application {
    public int run (String[] args) {
	shutdownOnInterrupt();

        communicator().addObjectFactory(new HelloFactory(),
					UCLM.HelloPersistent.ice_staticId());

	Ice.ObjectAdapter adapter = communicator().createObjectAdapter("OA");
        Freeze.Evictor evictor =
	    Freeze.Util.createBackgroundSaveEvictor(adapter, "db", "hello",
						    new HelloInitializer(),
						    null, true);
	for (int i=0; i<5; ++i) {
            Ice.Identity identity = Ice.Util.stringToIdentity("hello" + i);
            if (!evictor.hasObject(identity)) {
                Ice.ObjectPrx obj = evictor.add(new HelloI(), identity);
                System.out.println(communicator().proxyToString(obj));
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
