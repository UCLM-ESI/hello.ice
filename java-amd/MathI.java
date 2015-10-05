public final class MathI extends Example._MathDisp {
  public MathI(WorkQueue workQueue) {
    _workQueue = workQueue;
  }

  public void factorial_async(Example.AMD_Math_factorial cb,
  				int value, Ice.Current current) {
    _workQueue.add(cb, value);
  }

  private WorkQueue _workQueue;
}
