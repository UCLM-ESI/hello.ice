// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <Ice/Ice.h>
#include <HelloI.h>

using namespace std;
using namespace Ice;

class Server: public Application {
  int run(int argc, char* argv[]) {
    ObjectAdapterPtr adapter = communicator()->createObjectAdapter("OA");
    ObjectPrx prx = adapter->add(new UCLM::HelloI(),
							communicator()->stringToIdentity("hello1"));
    cout << communicator()->proxyToString(prx) << endl;

    adapter->activate();

    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    return 0;
  }
};


int main(int argc, char* argv[]) {
  Ice::Application* app = new Server();
  return app->main(argc, argv);
}
