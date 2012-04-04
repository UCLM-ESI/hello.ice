#include <Ice/Application.h>
#include <IceStorm/IceStorm.h>
#include <IceUtil/UUID.h>
#include "Hello.h"

using namespace std;
using namespace Ice;
using namespace IceStorm;
using namespace Example;


class HelloI : public Hello {
  void puts(const string& s, const Current& current) {
    cout << "Event received: " << s << endl;
  }
};

class Subscriber : public Application {
  TopicManagerPrx get_topic_manager() {
    string key = "IceStorm.TopicManager.Proxy";
    ObjectPrx base = communicator()->propertyToProxy(key);
    if (!base) {
      cerr << "property " << key << " not set." << endl;
      return 0;
    }

    cout << "Using IceStorm in: '" << key << "' " << endl;
    return TopicManagerPrx::checkedCast(base);
  }

public:
  virtual int run(int argc, char* argv[]) {
    TopicManagerPrx topic_mgr = get_topic_manager();
    if (!topic_mgr) {
      cerr << appName() << ": invalid proxy" << endl;
      return EXIT_FAILURE;
    }

    ObjectPtr servant = new HelloI;
    ObjectAdapterPtr adapter = \
      communicator()->createObjectAdapter("HelloAdapter");
    ObjectPrx subscriber = adapter->addWithUUID(servant);

    string topic_name = "HelloTopic";
    TopicPrx topic;
    try {
      topic = topic_mgr->retrieve(topic_name);
    } catch(const NoSuchTopic& e) {
      topic = topic_mgr->create(topic_name);
    }

    topic->subscribeAndGetPublisher(QoS(), subscriber);

    cout << "Waiting events... " << subscriber << endl;

    adapter->activate();
    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    topic->unsubscribe(subscriber);

    return EXIT_SUCCESS;
  }
};

int main(int argc, char* argv[]) {
  Subscriber app;
  return app.main(argc, argv);
}
