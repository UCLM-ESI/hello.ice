#include "Bool.h"
#include <Ice/Application.h>

using namespace std;
using namespace Ice;
using namespace IBool;

class MyApp: public Application {
public:
    virtual int run (int argc, char* argv[]) {
        ObjectPrx obj = communicator()->stringToProxy(argv[1]);
        RPrx r = RPrx::checkedCast(obj);
        cout << "previous value: " << r->get() << endl;
        WPrx w = WPrx::checkedCast(obj);
        Identity id;
        w->set(string("true") == argv[2], id);
        cout << "new value: " << r->get() << endl;
        return 0;
    }
};

int main (int argc, char* argv[]) {
  MyApp* app = new MyApp();
  app->main(argc, argv);
  exit(0);
}
