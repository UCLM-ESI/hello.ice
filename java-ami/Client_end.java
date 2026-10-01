import com.zeroc.Ice.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class Client_end extends Application {
  public int run(String[] args) {
    ObjectPrx proxy = communicator().stringToProxy(args[0]);
    Example.MathPrx math = Example.MathPrx.checkedCast(proxy);

    int value = Integer.parseInt(args[1]);
    CompletableFuture<Long> async_result = math.factorialAsync(value);
    System.out.println("that was an async call");

    try {
      System.out.println(async_result.get());
    } catch (InterruptedException | ExecutionException ex) {
      System.err.println("Exception is: " + ex);
      return 1;
    }
    return 0;
  }

  static public void main(String[] args) {
    if (args.length != 2) {
      System.err.println(appName() + ": usage: <server> <value>");
      return;
    }

    Client_end app = new Client_end();
    app.main("Client", args);
  }
}
