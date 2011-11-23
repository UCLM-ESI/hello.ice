public class Client extends Ice.Application {
    public int run (String[] args) {
	Ice.ObjectPrx obj = communicator().stringToProxy(args[0]);
	UCLM.HelloPrx prx = UCLM.HelloPrxHelper.checkedCast(obj);
	prx.puts("Hello, World!");
	return 0;
    }

    public static void main (String[] args) {
	Client app = new Client();
	app.main("Client", args);
	System.exit(0);
    }
}
