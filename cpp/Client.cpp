// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <Ice/Ice.h>
#include <Hello.h>
using namespace Ice;

class Client: public Ice::Application {
  int run(int argc, char* argv[]) {

    ObjectPrx obj = communicator()->stringToProxy(argv[1]);
    UCLM::HelloPrx hello = UCLM::HelloPrx::checkedCast(obj);
    hello->puts("Hello, World!");

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Ice::Application* app = new Client();
  return app->main(argc, argv);
}
