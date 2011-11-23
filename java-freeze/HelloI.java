
public class HelloI extends UCLM.HelloPersistent {
    public void puts(String str, Ice.Current current) {
	System.out.println("Hello (i=" + useCount + "): " + str);
        useCount += 1;
    }
}
