#include <Ice/Ice.h>
#include "factorial.h"

using namespace std;
using namespace Ice;

class Client: public Ice::Application {
  int run(int argc, char* argv[]) {
    ObjectPrx proxy = communicator()->stringToProxy(argv[1]);
    Example::MathPrx math = Example::MathPrx::checkedCast(proxy);

    Ice::AsyncResultPtr async_result = math->begin_factorial(atoi(argv[2]));
    cout << "that was an async call" << endl;

    cout << math->end_factorial(async_result) << endl;
    return 0;
  }
};


int main(int argc, char* argv[]) {
  if (argc != 3) {
    cerr << "usage: " << argv[0] << "<server> <value>" << endl;
    return 1;
  }

  Client app;
  return app.main(argc, argv);
}
