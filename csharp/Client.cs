using Ice;
using Example;

public class Client: Application {
  public override int run(string[] args) {
    ObjectPrx proxy = communicator().stringToProxy(args[0]);
    PrinterPrx printer = PrinterPrxHelper.checkedCast(proxy);

    printer.write("Hello, World!");

    return 0;
  }

  public static void Main(string[] args) {
    Application app = new Client();
    System.Environment.Exit(app.main(args));
  }
}
