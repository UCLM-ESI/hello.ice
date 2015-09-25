import Example.*;

class CallbackI extends _CallbackDisp implements java.lang.Runnable {
  private Ice.Communicator _broker;
  private boolean _destroy = false;
  private java.util.List<PrinterPrx> _clients =
    new java.util.ArrayList<PrinterPrx>();

  CallbackI(Ice.Communicator communicator) {
    _broker = communicator;
  }

  synchronized public void
  destroy() {
    System.out.println("destroying callback sender");
    _destroy = true;

    notify();

  }

  @Override
  public void
  attach(Ice.Identity ident, Ice.Current current) {
    System.out.println("new printer '" + _broker.identityToString(ident) + "'");

    Ice.ObjectPrx base = current.con.createProxy(ident);
    PrinterPrx client = PrinterPrxHelper.uncheckedCast(base);
    _clients.add(client);
  }

  @Override
  public void
  run() {
    int num = 0;

    while(true) {
      java.util.List<PrinterPrx> clients;

      synchronized(this) {
        try {
          wait(2000);
        }

        catch(java.lang.InterruptedException ex) {}

        if(_destroy)
          break;

        clients = new java.util.ArrayList<PrinterPrx>(_clients);
      }

      if(!clients.isEmpty()) {
        ++num;

        for(PrinterPrx remote_printer : clients) {
          try {
            remote_printer.write("text " + num);
          }

          catch(Ice.Exception ex) {
            System.out.println("removing client '" + _broker.identityToString(
                                 remote_printer.ice_getIdentity()) + "'");

            synchronized(this) {
              _clients.remove(remote_printer);
            }
          }
        }
      }

    }
  }
}
