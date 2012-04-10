import java.util.HashMap;
import Ice.*;
import IceStorm.*;
import Example.*;

public class Subscriber extends Application {
    public class HelloI extends _HelloDisp {
        public void puts(String message, Ice.Current current) {
            System.out.println(message);
        }
    }

    public int run(String[] args) {
	String key = "IceStorm.TopicManager.Proxy";
	ObjectPrx prx = communicator().propertyToProxy(key);
	TopicManagerPrx manager = TopicManagerPrxHelper.checkedCast(prx);

        if(manager == null) {
            System.err.println("invalid proxy");
            return 1;
        }

	HelloI servant = new HelloI();
        ObjectAdapter adapter =
	    communicator().createObjectAdapter("HelloAdapter");
        ObjectPrx subscriber = adapter.addWithUUID(servant);

        String topic_name = "HelloTopic";
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
            topic.subscribeAndGetPublisher(new HashMap<String,String>(),
					   subscriber);
        } catch(AlreadySubscribed e) {
            e.printStackTrace();
            return 1;
        } catch(BadQoS e) {
            e.printStackTrace();
            return 1;
        }

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
