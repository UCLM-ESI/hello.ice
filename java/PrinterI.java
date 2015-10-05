public final class PrinterI extends Example._PrinterDisp {
    public PrinterI() {}

    public void write(String message, Ice.Current current) {
        System.out.println(message);
    }
}
