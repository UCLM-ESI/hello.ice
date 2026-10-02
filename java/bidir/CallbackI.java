import com.zeroc.Ice.Current;
import com.zeroc.Ice.Identity;
import com.zeroc.Ice.Util;
import Example.*;

class CallbackI implements Callback, java.lang.Runnable {
  private boolean _destroy = false;
  private java.util.List<PrinterPrx> _clients =
    new java.util.ArrayList<PrinterPrx>();

  synchronized public void
  destroy() {
    System.out.println("destroying callback sender");
    _destroy = true;

    notify();
  }

  @Override
  synchronized public void
  attach(Identity ident, Current current) {
    System.out.println("new printer '" + Util.identityToString(ident) + "'");

    PrinterPrx client = PrinterPrx.uncheckedCast(current.con.createProxy(ident));
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

          catch(com.zeroc.Ice.LocalException ex) {
            System.out.println("removing client '" + Util.identityToString(
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
