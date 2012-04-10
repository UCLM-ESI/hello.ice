public class Client_end extends Ice.Application {
  public int run(String[] args) {
    Ice.ObjectPrx proxy = communicator().stringToProxy(args[0]);
    Example.MathPrx math = Example.MathPrxHelper.checkedCast(proxy);

    System.out.println(Long.toString(math.factorial(Integer.parseInt(args[1]))));

    return 0;
  }

  static public void main(String[] args) {
    Client_end app = new Client_end();
    app.main("Client", args);
  }
}
