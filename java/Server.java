public class Server extends com.zeroc.Ice.Application {
    public int run(String[] args) {
        com.zeroc.Ice.Object servant = new PrinterI();

        com.zeroc.Ice.ObjectAdapter adapter = 
            communicator().createObjectAdapter("PrinterAdapter");
	    com.zeroc.Ice.ObjectPrx proxy = 
            adapter.add(servant, com.zeroc.Ice.Util.stringToIdentity("printer1"));
        
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
