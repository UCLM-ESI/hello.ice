import com.zeroc.Ice.*;

public class Client extends Application {
  public int run(String[] args) {
    ObjectPrx obj = communicator().stringToProxy(args[0]);
    Example.PrinterPrx printer = Example.PrinterPrx.checkedCast(obj);

    printer.write("Hello World!");

    return 0;
  }

  static public void main(String[] args) {
    Client app = new Client();
    app.main("Client", args);
  }
}
