import com.zeroc.Ice.*;

public class Server extends Application {
  public int run(String[] args) {
    CallbackI servant = new CallbackI();

    ObjectAdapter adapter =
      communicator().createObjectAdapter("CallbackAdapter");
    ObjectPrx proxy =
      adapter.add(servant, Util.stringToIdentity("callback"));

    System.out.println(communicator().proxyToString(proxy));

    adapter.activate();

    Thread thread = new Thread(servant);
    thread.start();

    shutdownOnInterrupt();
    try {
      communicator().waitForShutdown();
    }

    finally {
      servant.destroy();

      try {
        thread.join();
      }

      catch(java.lang.InterruptedException ex) {}
    }

    return 0;
  }

  static public void main(String[] args) {
    Server app = new Server();
    app.main("Server", args);
  }
}
