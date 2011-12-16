#include <Ice/Application.h>
#include <IceStorm/IceStorm.h>

#include "Hello.h"

using namespace std;
using namespace Ice;
using namespace IceStorm;
using namespace UCLM;

class Publisher : public Application {

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
  virtual int run(int argc, char*[]) {

    TopicManagerPrx topic_mgr = get_topic_manager();
    if (!topic_mgr) {
      cerr << appName() << ": invalid proxy" << endl;
      return EXIT_FAILURE;
    }


    TopicPrx topic;
    try {
      topic = topic_mgr->retrieve("HelloTopic");
    }
    catch (const NoSuchTopic& e) {
      cerr << appName() << ": no sucho topic found, created" << endl;
      topic = topic_mgr->create("HelloTopic");
    }

    assert(topic);

    // Get the topic's publisher object.
    ObjectPrx prx = topic->getPublisher();
    HelloPrx hello = HelloPrx::uncheckedCast(prx);

    cout << "publishing 10 'Hello World' events" << endl;
    for (int i = 0; i < 10; ++i) {
      hello->puts("Hello World!");
    }

    return EXIT_SUCCESS;
  }
};

int main(int argc, char* argv[]) {
  Publisher app;
  return app.main(argc, argv);
}
