#include <Ice/Ice.h>
#include <factorial.h>

using namespace std;
using namespace Ice;
using namespace Example;

class FactorialCB : public IceUtil::Shared {
public:
  void response(const Ice::Long retval) {
    cout << "Callback: Value is " << retval << endl;
  }

  void failure(const Exception& ex) {
    cout << "Exception is: " << ex << endl;
  }
};

class Client: public Ice::Application {
public:
  int run(int argc, char* argv[]) {

    ObjectPrx proxy = communicator()->stringToProxy(argv[1]);
    MathPrx math = MathPrx::checkedCast(proxy);

    Callback_Math_factorialPtr factorial_cb =
      newCallback_Math_factorial(new FactorialCB,
				 &FactorialCB::response,
				 &FactorialCB::failure);

    math->begin_factorial(atoi(argv[2]), factorial_cb);
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
