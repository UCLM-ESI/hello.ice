import com.zeroc.Ice.*;

public class Client extends Application {
    public int run(String[] args) {
	ObjectPrx proxy = communicator().stringToProxy(args[0]);
	Example.MathPrx math = Example.MathPrx.checkedCast(proxy);

	System.out.println(math.factorial(Integer.parseInt(args[1])));

	return 0;
    }

    static public void main(String[] args) {
	Client app = new Client();
	app.main("Client", args);
    }
}
