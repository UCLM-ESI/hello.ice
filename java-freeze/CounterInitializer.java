public class CounterInitializer
    implements Freeze.ServantInitializer {

    public void initialize(
        Ice.ObjectAdapter adapter, Ice.Identity identity,
	String str, Ice.Object obj)
    {
	CounterI counter = (CounterI)obj;
	System.out.println(identity.name + " Initial: " + counter.status);
    }
}
