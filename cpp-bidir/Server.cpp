#include <Ice/Ice.h>
#include "CallbackI.h"

using namespace std;
using namespace Ice;

class Server: public Application {
  int run(int argc, char* argv[]) {
    Example::CallbackIPtr servant = new Example::CallbackI(communicator());

    ObjectAdapterPtr adapter =
         communicator()->createObjectAdapter("CallbackAdapter");
    ObjectPrx proxy = adapter->add(
	 servant, communicator()->stringToIdentity("callback"));

    cout << communicator()->proxyToString(proxy) << endl;

    adapter->activate();

    servant->start();
    shutdownOnInterrupt();
    communicator()->waitForShutdown();
    servant->destroy();

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Server app;
  return app.main(argc, argv);
}
