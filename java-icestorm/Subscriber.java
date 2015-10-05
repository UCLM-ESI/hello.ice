import java.util.HashMap;
import Ice.*;
import IceStorm.*;
import Example.*;

public class Subscriber extends Application {
  public class PrinterI extends _PrinterDisp {
    public void write(String message, Ice.Current current) {
      System.out.println(String.format("Event received: %s", message));
    }
  }

  public int run(String[] args) {
    String key = "IceStorm.TopicManager.Proxy";
    ObjectPrx prx = communicator().propertyToProxy(key);
    TopicManagerPrx manager = TopicManagerPrxHelper.checkedCast(prx);

    if (manager == null) {
      System.err.println("invalid proxy");
      return 1;
    }

    PrinterI servant = new PrinterI();
    ObjectAdapter adapter =
	   communicator().createObjectAdapter("PrinterAdapter");
    ObjectPrx subscriber = adapter.addWithUUID(servant);

    String topic_name = "PrinterTopic";
    TopicPrx topic;
    try {
      topic = manager.retrieve(topic_name);
    } catch(NoSuchTopic e) {
      try {
        topic = manager.create(topic_name);
      } catch(TopicExists ex) {
        System.err.println("Temporary failure, try again.");
        return 1;
      }
    }

    try {
      topic.subscribeAndGetPublisher(null, subscriber);
    } catch(InvalidSubscriber e) {
      e.printStackTrace();
      return 1;
    } catch(AlreadySubscribed e) {
      e.printStackTrace();
      return 1;
    } catch(BadQoS e) {
      e.printStackTrace();
      return 1;
    }

    System.out.println("Waiting events... ");

    adapter.activate();
    shutdownOnInterrupt();
    communicator().waitForShutdown();

    topic.unsubscribe(subscriber);

    return 0;
  }

  public static void main(String[] args) {
    Subscriber app = new Subscriber();
    int status = app.main("Subscriber", args);
    System.exit(status);
  }
}
