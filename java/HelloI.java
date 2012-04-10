public final class HelloI extends Example._HelloDisp {
    public HelloI() {}

    public void puts(String message, Ice.Current current) {
	System.out.println(message);
    }
}
