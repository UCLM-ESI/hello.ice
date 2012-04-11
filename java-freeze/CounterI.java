public class CounterI extends Counter.RWPersistent {
    public int get(Ice.Current current) {
        return status;
    }
    public void set(int value, Ice.Current current) {
        status = value;
	System.out.println("Value set to " + status);
    }
    public void inc(Ice.Current current) {
        status += 1;
	System.out.println("Value set to " + status);
    }
}
