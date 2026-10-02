import com.zeroc.Ice.Current;

public final class MathI implements Example.Math
{
    public MathI() { }

    public long factorial_(int n) {
	if (n == 0)
	    return 1;

	return n * factorial_(n-1);
    }

    @Override
    public long
    factorial(int value, Current current) {
        return factorial_(value);
    }
}
