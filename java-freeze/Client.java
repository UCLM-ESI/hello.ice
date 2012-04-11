public class Client extends Ice.Application {
    public int run (String[] args) {
	Ice.ObjectPrx proxy = communicator().stringToProxy(args[0]);
	Counter.WPrx counter = Counter.WPrxHelper.checkedCast(proxy);
	counter.set(5);
	return 0;
    }

    public static void main (String[] args) {
	Client app = new Client();
	System.exit(app.main("Client", args));
    }
}
