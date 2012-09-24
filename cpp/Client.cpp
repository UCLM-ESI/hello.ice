#include <Ice/Ice.h>
#include "Printer.h"

using namespace Ice;
using namespace Example;

class Client: public Ice::Application {
  int run(int argc, char* argv[]) {
    ObjectPrx proxy = communicator()->stringToProxy(argv[1]);
    PrinterPrx printer = PrinterPrx::checkedCast(proxy);

    printer->write("Hello, World!");

    return 0;
  }
};

int main(int argc, char* argv[]) {
  Client app;
  return app.main(argc, argv);
}
