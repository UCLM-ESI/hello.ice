#include <Ice/Ice.h>
#include "counter.h"

using namespace std;
using namespace Ice;
using namespace Example;

class Client: public Application {
  int run(int argc, char* argv[]) {
    ObjectPrx proxy = communicator()->stringToProxy(argv[1]);
    CounterPrx counter = CounterPrx::checkedCast(proxy);

    if (!counter)
      throw runtime_error("invalid proxy");

    counter->create("counter1");
    counter->increment("counter1", 5);
    cout << "After incrementing counter1 by 5: " << counter->get("counter1") << endl;

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Client app;
  return app.main(argc, argv);
}
