using Ice;
using Example;

public class PrinterI: PrinterDisp_ {
  public override void write(string message, Current current) {
    System.Console.Out.WriteLine(message);
  }
}

public class Server: Application {
  public override int run(string[] args) {
    PrinterI servant = new PrinterI();

    ObjectAdapter adapter = communicator().createObjectAdapter("PrinterAdapter");
    ObjectPrx proxy = adapter.add(servant, Util.stringToIdentity("printer1"));

    System.Console.WriteLine(communicator().proxyToString(proxy));

    adapter.activate();
    shutdownOnInterrupt();
    communicator().waitForShutdown();

    return 0;
  }

  public static void Main(string[] args) {
    Application app = new Server();
    System.Environment.Exit(app.main(args));
  }
}
