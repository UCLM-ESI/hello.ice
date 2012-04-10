#include <Ice/Ice.h>
#include "HelloI.h"

using namespace std;
using namespace Ice;

class Server: public Application {
  int run(int argc, char* argv[]) {
	Example::HelloPtr servant = new Example::HelloI();

    ObjectAdapterPtr adapter = \
        communicator()->createObjectAdapter("HelloAdapter");
	ObjectPrx proxy = adapter->add(
        servant, communicator()->stringToIdentity("hello1"));

    cout << communicator()->proxyToString(proxy) << endl;

    adapter->activate();
    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Server app;
  return app.main(argc, argv);
}
