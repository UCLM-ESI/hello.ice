#include <Ice/Application.h>
#include <IceStorm/IceStorm.h>
#include "Printer.h"

using namespace std;
using namespace Ice;
using namespace IceStorm;
using namespace Example;

class Publisher : public Application {
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
  virtual int run(int argc, char*[]) {
    TopicManagerPrx topic_mgr = get_topic_manager();
    if (!topic_mgr) {
      cerr << appName() << ": invalid proxy" << endl;
      return EXIT_FAILURE;
    }

    string topic_name = "PrinterTopic";
    TopicPrx topic;
    try {
      topic = topic_mgr->retrieve(topic_name);
    } catch (const NoSuchTopic& e) {
      cerr << appName()
	   << ": no sucho topic found, creating" << endl;
      topic = topic_mgr->create(topic_name);
    }

    assert(topic);

    ObjectPrx publisher = topic->getPublisher();
    PrinterPrx printer = PrinterPrx::uncheckedCast(publisher);

    cout << "publishing 10 'Hello World' events" << endl;
    for(char i='0'; i <= '9'; ++i)
      printer->write(string("Hello World ") + i + "!");

    return EXIT_SUCCESS;
  }
};

int main(int argc, char* argv[]) {
  Publisher app;
  return app.main(argc, argv);
}
