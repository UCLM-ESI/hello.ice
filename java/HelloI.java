
package Example;

public final class HelloI extends _HelloDisp
{
    public HelloI() {}

    public void puts(String message, Ice.Current current) {
	System.out.println(message);
    }
}
