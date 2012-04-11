#include <Ice/Ice.h>
#include "factorialI.h"

using namespace std;
using namespace Ice;

class Server: public Ice::Application {
  int run(int argc, char* argv[]) {
	Example::MathPtr servant = new Example::MathI();

    ObjectAdapterPtr adapter = \
	  communicator()->createObjectAdapter("HelloAdapter");
    ObjectPrx prx = adapter->add(
      servant, communicator()->stringToIdentity("hello1"));

    cout << communicator()->proxyToString(prx) << endl;

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
