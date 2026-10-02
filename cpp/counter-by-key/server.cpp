#include <Ice/Ice.h>
#include "counter.h"

using namespace std;
using namespace Ice;
using namespace Example;

class CounterI: public Counter {
  CounterDict counters;

public:
  void create(const string& name, const Current& current) {
    cerr << "Received request to create counter: " << name << endl;
    if (counters.count(name)) {
      cerr << "Counter " << name << " already exists" << endl;
      return;
    }

    counters[name] = 0;
  }

  void increment(const string& name, Long delta, const Current& current) {
    cerr << "Received request to increment " << name << " by " << delta << endl;
    if (!counters.count(name))
      throw NotFound(name);

    counters[name] += delta;
  }

  Long get(const string& name, const Current& current) {
    cerr << "Received request to get counter: " << name << endl;
    if (!counters.count(name))
      throw NotFound(name);

    return counters[name];
  }

  CounterDict list(const Current& current) {
    cerr << "Received request to list counters" << endl;
    return counters;
  }
};

class Server: public Application {
  int run(int argc, char* argv[]) {
    ObjectAdapterPtr adapter =
      communicator()->createObjectAdapter("CounterAdapter");

    ObjectPrx proxy = adapter->add(new CounterI(), stringToIdentity("counter"));

    cout << communicator()->proxyToString(proxy) << endl;

    adapter->activate();
    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Server app;
  return app.main(argc, argv);
}
