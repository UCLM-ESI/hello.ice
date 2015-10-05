class FactorialCB extends Example.Callback_Math_factorial {
  public void response(long value) {
    System.out.println("Callback: Value is: " + value);
  }

  public void exception(Ice.LocalException ex) {
    System.err.println("Exception is: " + ex);
  }
}

public class Client_callback extends Ice.Application {
  public int run(String[] args) {
    Ice.ObjectPrx proxy = communicator().stringToProxy(args[0]);
    Example.MathPrx math = Example.MathPrxHelper.checkedCast(proxy);

    FactorialCB factorial_cb = new FactorialCB();
    math.begin_factorial(Integer.parseInt(args[1]), factorial_cb);
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
