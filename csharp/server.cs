using System;
using Example;

public class PrinterI : PrinterDisp_ {
  public override void write(string message, Ice.Current current) {
    Console.WriteLine(message);
  }
}

public class Server {
  public static int Main(string[] args) {
    using (Ice.Communicator communicator = Ice.Util.initialize(ref args)) {
      Console.CancelKeyPress += (sender, eventArgs) => {
        eventArgs.Cancel = true;
        communicator.shutdown();
      };

      Ice.ObjectAdapter adapter =
        communicator.createObjectAdapter("PrinterAdapter");
      Ice.ObjectPrx proxy =
        adapter.add(new PrinterI(), Ice.Util.stringToIdentity("printer1"));

      Console.WriteLine(communicator.proxyToString(proxy));

      adapter.activate();
      communicator.waitForShutdown();
    }
    return 0;
  }
}
