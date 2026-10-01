import com.zeroc.Ice.Current;

public final class PrinterI implements Example.Printer {
    public PrinterI() {}

    @Override
    public void write(String message, Current current) {
        System.out.println(message);
    }
}
