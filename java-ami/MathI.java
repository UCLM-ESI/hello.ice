public final class MathI extends Example._MathDisp
{
    public MathI() { }

    public long factorial_(int n) {
	if (n == 0)
	    return 1;

	return n * factorial_(n-1);
    }

    public long
    factorial(int value, Ice.Current current) {
        return factorial_(value);
    }
}
