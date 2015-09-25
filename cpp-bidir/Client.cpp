#include <Ice/Ice.h>
#include <Callback.h>
#include <Printer.h>
#include <PrinterI.h>

using namespace Ice;

class Client: public Application {
  int run(int argc, char* argv[]) {
    Example::PrinterPtr servant = new Example::PrinterI();

    ObjectAdapterPtr adapter =
         communicator()->createObjectAdapter("");
    ObjectPrx proxy = adapter->addWithUUID(servant);
    adapter->activate();

    ObjectPrx server_proxy = communicator()->stringToProxy(argv[1]);
    Example::CallbackPrx server = Example::CallbackPrx::checkedCast(server_proxy);

    server->ice_getConnection()->setAdapter(adapter);
    server->attach(proxy->ice_getIdentity());

    shutdownOnInterrupt();
    communicator()->waitForShutdown();

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Client app;
  return app.main(argc, argv);
}
