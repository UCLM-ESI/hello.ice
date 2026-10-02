using System;
using Example;

public class Client {
  public static int Main(string[] args) {
    using (Ice.Communicator communicator = Ice.Util.initialize(ref args)) {
      if (args.Length != 1) {
        Console.Error.WriteLine("usage: client <proxy>");
        return 1;
      }

      Ice.ObjectPrx proxy = communicator.stringToProxy(args[0]);
      PrinterPrx printer = PrinterPrxHelper.checkedCast(proxy);
      if (printer == null) {
        Console.Error.WriteLine("invalid proxy");
        return 1;
      }

      printer.write("Hello World!");
    }
    return 0;
  }
}
