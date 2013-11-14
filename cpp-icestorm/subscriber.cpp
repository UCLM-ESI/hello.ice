#include <Ice/Application.h>
#include <IceStorm/IceStorm.h>
#include <IceUtil/UUID.h>
#include "Printer.h"

using namespace std;
using namespace Ice;
using namespace IceStorm;
using namespace Example;


class PrinterI : public Printer {
public:
  void write(const string& message, const Current& current) {
    cout << "Event received: " << message << endl;
  }
};


class Subscriber : public Application {
  TopicManagerPrx get_topic_manager() {
    string key = "IceStorm.TopicManager.Proxy";
    ObjectPrx proxy = communicator()->propertyToProxy(key);
    if (!proxy) {
      cerr << "property " << key << " not set." << endl;
      return 0;
    }

    cout << "Using IceStorm in: '" << key << "' " << endl;
    return TopicManagerPrx::checkedCast(proxy);
  }

public:
  virtual int run(int argc, char* argv[]) {
    TopicManagerPrx topic_mgr = get_topic_manager();
    if (!topic_mgr) {
      cerr << appName() << ": invalid proxy" << endl;
      return EXIT_FAILURE;
    }

    ObjectPtr servant = new PrinterI;
    ObjectAdapterPtr adapter = \
      communicator()->createObjectAdapter("PrinterAdapter");
    ObjectPrx subscriber = adapter->addWithUUID(servant);

    string topic_name = "PrinterTopic";
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
