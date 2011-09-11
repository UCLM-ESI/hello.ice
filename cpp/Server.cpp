// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <Ice/Ice.h>
#include <HelloI.h>
using namespace Ice;

class Server: public Ice::Application {
  int run(int argc, char* argv[]) {

    ObjectAdapterPtr oa = communicator()->createObjectAdapter("OA");
    ObjectPrx prx = oa->add(new UCLM::HelloI(),
							communicator()->stringToIdentity("hello1"));
    oa->activate();

    std::cout << communicator()->proxyToString(prx) << std::endl;

    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    return 0;
  }
};


int main(int argc, char* argv[]) {
  Ice::Application* app = new Server();
  return app->main(argc, argv);
}
