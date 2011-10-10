#include "BoolFactory.h"
#include <Ice/Application.h>

using namespace std;
using namespace Ice;
using namespace IBool;

class MyApp: public Application {
public:
    virtual int run (int argc, char* argv[]) {
        ObjectPrx obj = communicator()->stringToProxy(argv[1]);
        RWRemoteFactoryPrx f = RWRemoteFactoryPrx::checkedCast(obj);
        cout << communicator()->proxyToString(f->create()) << endl;
        return 0;
    }
};

int main (int argc, char* argv[]) {
  MyApp* app = new MyApp();
  app->main(argc, argv);
  exit(0);
}
