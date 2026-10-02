import com.zeroc.Ice.*;

public class Client extends Application {
  public int run(String[] args) {
    PrinterI servant = new PrinterI();

    ObjectAdapter adapter =
      communicator().createObjectAdapter("");
    ObjectPrx proxy = adapter.addWithUUID(servant);
    adapter.activate();

    ObjectPrx server_proxy = communicator().stringToProxy(args[0]);
    Example.CallbackPrx server = Example.CallbackPrx.checkedCast(server_proxy);

    server.ice_getConnection().setAdapter(adapter);
    server.attach(proxy.ice_getIdentity());

    shutdownOnInterrupt();
    communicator().waitForShutdown();

    return 0;
  }

  static public void main(String[] args) {
    Client app = new Client();
    app.main("Client", args);
  }
}
