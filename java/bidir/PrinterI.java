import com.zeroc.Ice.Current;

public final class PrinterI implements Example.Printer {
  private int num = 0;
  public PrinterI() {}

  @Override
  public void write(String message, Current current) {
    num++;
    System.out.println(num + ": " + message);
  }
}
