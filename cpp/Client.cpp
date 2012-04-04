// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <Ice/Ice.h>
#include "Hello.h"

using namespace Ice;
using namespace Example;

class Client: public Ice::Application {
  int run(int argc, char* argv[]) {
    ObjectPrx proxy = communicator()->stringToProxy(argv[1]);
    HelloPrx hello = HelloPrx::checkedCast(proxy);

    hello->puts("Hello, World!");

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Client app;
  return app.main(argc, argv);
}
