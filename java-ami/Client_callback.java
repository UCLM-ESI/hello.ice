import com.zeroc.Ice.*;

public class Client_callback extends Application {
  public int run(String[] args) {
    ObjectPrx proxy = communicator().stringToProxy(args[0]);
    Example.MathPrx math = Example.MathPrx.checkedCast(proxy);

    math.factorialAsync(Integer.parseInt(args[1])).whenComplete((result, ex) -> {
      if (ex != null) {
        System.err.println("Exception is: " + ex);
      } else {
        System.out.println("Callback: Value is: " + result);
      }
    });
    return 0;
  }

  static public void main(String[] args) {
    if (args.length != 2) {
      System.err.println(appName() + ": usage: <server> <value>");
      return;
    }

    Client_callback app = new Client_callback();
    app.main("Client", args);
  }
}
