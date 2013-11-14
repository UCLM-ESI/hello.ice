import Ice.*;
import IceStorm.*;
import Example.*;

public class Publisher extends Application {
  public int run(String[] args) {
    String key = "IceStorm.TopicManager.Proxy";
    ObjectPrx prx = communicator().propertyToProxy(key);
    TopicManagerPrx manager = TopicManagerPrxHelper.checkedCast(prx);

    if (manager == null) {
      System.err.println("invalid proxy");
      return 1;
    }

    String topicName = "PrinterTopic";
    TopicPrx topic;
    try {
      topic = manager.retrieve(topicName);
    } catch(NoSuchTopic e) {
      try {
        topic = manager.create(topicName);
      } catch(TopicExists ex) {
        System.err.println("Temporary failure, try again.");
        return 1;
      }
    }

    ObjectPrx publisher = topic.getPublisher();
    PrinterPrx printer = PrinterPrxHelper.uncheckedCast(publisher);

    System.out.println("publishing 10 'Hello World' events");
    for(int i=0; i < 10; i++)
       printer.write(String.format("Hello World %s!", i));

    return 0;
  }

  public static void main(String[] args) {
    Publisher app = new Publisher();
    int status = app.main("Publisher", args);
    System.exit(status);
  }
}
