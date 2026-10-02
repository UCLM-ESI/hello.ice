#include <Ice/Ice.h>
#include "counter.h"

using namespace std;
using namespace Ice;

class CounterI: public Example::Counter {
  Long value;

public:
  CounterI(): value(0) {}

  Long increment(const Current& current) {
    return ++value;
  }

  Long get(const Current& current) {
    return value;
  }
};

class Server: public Application {
  int run(int argc, char* argv[]) {
    ObjectAdapterPtr adapter =
      communicator()->createObjectAdapter("CounterAdapter");

    ObjectPrx proxy1 = adapter->add(new CounterI(), stringToIdentity("counter1"));
    ObjectPrx proxy2 = adapter->add(new CounterI(), stringToIdentity("counter2"));

    cout << communicator()->proxyToString(proxy1) << endl;
    cout << communicator()->proxyToString(proxy2) << endl;

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
