#include "BoolPersistent.h"
#include <Ice/Application.h>
#include <IceUtil/IceUtil.h>

using namespace std;
using namespace Ice;
using namespace IBool;

namespace IBool {

class WI : public W
{
public:
    virtual void set(bool v,
                     const Identity&,
                     const Current&) {
        cout << "new value: " << v << endl;
    }
};

}


class MyApp: public Application {
public:
    virtual int run (int argc, char* argv[]) {
        ObjectAdapterPtr oa = communicator()->createObjectAdapter("OA");
        ObjectPrx obj = communicator()->stringToProxy(argv[1]);
        ObservablePrx o = ObservablePrx::checkedCast(obj);
        ObjectPrx listener = oa->addWithUUID(new WI());
        o->addListener(WPrx::uncheckedCast(listener));
        oa->activate();
        communicator()->waitForShutdown();
        return 0;
    }
};

int main (int argc, char* argv[]) {
  MyApp* app = new MyApp();
  app->main(argc, argv);
  exit(0);
}
