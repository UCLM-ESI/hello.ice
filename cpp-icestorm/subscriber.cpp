#include <Ice/Application.h>
#include <IceStorm/IceStorm.h>
#include <IceUtil/UUID.h>
#include "Hello.h"

using namespace std;
using namespace Ice;
using namespace IceStorm;
using namespace UCLM;


class HelloI : public Hello {
  void puts(const string& s, const Current& current) {
    cout << "Event received: " << s << endl;
  }
};

class Subscriber : public Application {

  TopicManagerPrx get_topic_manager() {
    string key = "IceStormAdmin.TopicManager.Default";
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

    // Create the servant to receive the events.
    ObjectAdapterPtr adapter = communicator()->createObjectAdapter("Hello.Subscriber");
    ObjectPtr servant = new HelloI;

    // Add a Servant for the Ice Object.
    ObjectPrx base = adapter->addWithUUID(servant);
    TopicPrx topic;

    try {
      topic = topic_mgr->retrieve("HelloTopic");
      QoS qos;
      topic->subscribeAndGetPublisher(qos, base);
    }
    catch(const NoSuchTopic& e) {
      cerr << appName() << ": " << e << " name: " << e.name << endl;
      return EXIT_FAILURE;
    }

    cout << "Waiting events... " << base << endl;

    adapter->activate();
    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    topic->unsubscribe(base);

    return EXIT_SUCCESS;
  }
};

int main(int argc, char* argv[]) {
  Subscriber app;
  return app.main(argc, argv);
}
