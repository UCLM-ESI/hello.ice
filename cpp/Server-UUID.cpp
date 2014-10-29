#include <Ice/Ice.h>
#include "PrinterI.h"

using namespace std;
using namespace Ice;

class Server: public Application {
  int run(int argc, char* argv[]) {
    Example::PrinterPtr servant = new Example::PrinterI();

    ObjectAdapterPtr adapter =
         communicator()->createObjectAdapter("PrinterAdapter");
    ObjectPrx proxy = adapter->addWithUUID(servant);

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
