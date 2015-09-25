public final class PrinterI extends Example._PrinterDisp {
  private int num = 0;
  public PrinterI() {}

  public void write(String message, Ice.Current current) {
    num++;
    System.out.println(num + ": " + message);
  }
}
