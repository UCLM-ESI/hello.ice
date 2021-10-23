import Example.*;

public final class PrinterI implements Printer {
    public PrinterI() {}

    @Override
    public void write(String message, com.zeroc.Ice.Current current) {
        System.out.println(message);
    }
}
