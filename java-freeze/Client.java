public class Client extends Ice.Application {
    public int run (String[] args) {
	Ice.ObjectPrx proxy = communicator().stringToProxy(args[0]);

	Counter.RPrx counter_reader = Counter.RPrxHelper.checkedCast(proxy);
	System.out.println("Current value: " + counter_reader.get());

	Counter.WPrx counter_writer = Counter.WPrxHelper.checkedCast(proxy);
	counter_writer.set(5);
	return 0;
    }

    public static void main (String[] args) {
	Client app = new Client();
	System.exit(app.main("Client", args));
    }
}
