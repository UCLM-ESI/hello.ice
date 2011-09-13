public final class HelloI extends UCLM._HelloDisp
{
    public HelloI() {}

    public void
    puts(String str, Ice.Current __current) {
	System.out.println(str);
    }
}
