import Ice.*;

public class Server extends Ice.Application {
  class ShutdownHook extends Thread {
    public void run() {
      _workQueue._destroy();
      communicator().shutdown();
    }
  }

  public int run(String[] args) {
    setInterruptHook(new ShutdownHook());

    _workQueue = new WorkQueue();
    MathI servant = new MathI(_workQueue);

    ObjectAdapter adapter =
      communicator().createObjectAdapter("MathAdapter");
    ObjectPrx math = adapter.add(
      servant, Util.stringToIdentity("math1"));

    System.out.println(communicator().proxyToString(math));

    _workQueue.start();
    adapter.activate();
    communicator().waitForShutdown();

    try {
      _workQueue.join();
    } catch(java.lang.InterruptedException ex) {}

    return 0;
  }

  static public void main(String[] args) {
    Server app = new Server();
    app.main("Server", args);
  }

  private WorkQueue _workQueue;
}
