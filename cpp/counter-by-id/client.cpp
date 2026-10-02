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

    cout << "get() = '" << counter->get() << "'" << endl;
    cout << "increment() = '" << counter->increment() << "'" << endl;
    cout << "increment() = '" << counter->increment() << "'" << endl;
    cout << "get() = '" << counter->get() << "'" << endl;

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Client app;
  return app.main(argc, argv);
}
