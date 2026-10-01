#include <Ice/Ice.h>
#include "counter.h"

using namespace std;

class Client: public Ice::Application {
public:
  virtual int run (int argc, char* argv[]) {
    Ice::ObjectPrx proxy = communicator()->stringToProxy(argv[1]);

    Counter::RPrx counter_reader = Counter::RPrx::checkedCast(proxy);
    cout << "Current value: " << counter_reader->get() << endl;

    Counter::WPrx counter_writer = Counter::WPrx::checkedCast(proxy);
    counter_writer->set(5);

    return 0;
  }
};

int main (int argc, char* argv[]) {
  Client app;
  return app.main(argc, argv);
}
