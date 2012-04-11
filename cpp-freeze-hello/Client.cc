#include <Ice/Ice.h>
#include <Hello.h>

using namespace std;
using namespace UCLM;

class Client: public Ice::Application {
public:
  virtual int run (int argc, char* argv[]) {
    Ice::ObjectPrx obj = communicator()->stringToProxy(argv[1]);
    UCLM::HelloPrx prx = UCLM::HelloPrx::checkedCast(obj);
    prx->puts("Hello, World!");
    return 0;
  }
};

int main (int argc, char* argv[]) {
  Client* app = new Client();
  app->main(argc, argv);
  exit(0);
}
