import com.zeroc.Ice.Current;
import java.util.concurrent.CompletionStage;
import java.util.concurrent.CompletableFuture;

public final class MathI implements Example.Math {
  public MathI(WorkQueue workQueue) {
    _workQueue = workQueue;
  }

  @Override
  public CompletionStage<Long> factorialAsync(int value, Current current) {
    CompletableFuture<Long> future = new CompletableFuture<>();
    _workQueue.add(future, value);
    return future;
  }

  private WorkQueue _workQueue;
}
