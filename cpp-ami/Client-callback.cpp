// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <Ice/Ice.h>
#include <factorial.h>

using namespace Ice;
using namespace std;


class FCallback : public IceUtil::Shared {
public:
  void factorialCB(const string& retval) {
    cout << "Value is: " << retval << endl;
  }

  void failureCB(const Exception& ex) {
    cout << "Exception is: " << ex << endl;
  }
};

typedef IceUtil::Handle<FCallback> FCallbackPtr;

class Client: public Ice::Application {
protected:

  int run(int argc, char* argv[]) {
    
    ObjectPrx obj = communicator()->stringToProxy(argv[1]);
    UCLM::MathPrx prx = UCLM::MathPrx::checkedCast(obj);

    FCallbackPtr cb = new FCallback;

    UCLM::Callback_Math_factorialPtr factorialCB = 
      UCLM::newCallback_Math_factorial(cb, &FCallback::factorialCB, &FCallback::failureCB);
    
    prx->begin_factorial(atoi(argv[2]), factorialCB);
    return 0;
  }

};


int main(int argc, char* argv[]) {
  if (argc != 3) {
    cerr << "usage: " << argv[0] << "<server> <value>" << endl;
    return 1;
  }

  Ice::Application* app = new Client();
  return app->main(argc, argv);
}

