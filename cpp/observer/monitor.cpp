#include <Ice/Ice.h>
#include "BoolObservable.h"

using namespace std;
using namespace Ice;
using namespace IBool;

namespace IBool {

class WI : public W {
public:
    virtual void set(bool v, const Identity&, const Current&) {
        cout << "new value: " << v << endl;
    }
};

}


class MyApp: public Application {
public:
    virtual int run(int argc, char* argv[]) {
        if (argc != 2) {
            cerr << "usage: " << appName() << " <bool-proxy>" << endl;
            return EXIT_FAILURE;
        }

        ObjectAdapterPtr oa = communicator()->createObjectAdapter("OA");
        WPrx listener = WPrx::uncheckedCast(oa->addWithUUID(new WI()));
        oa->activate();

        ObjectPrx obj = communicator()->stringToProxy(argv[1]);
        ObservablePrx observable = ObservablePrx::checkedCast(obj);
        observable->addListener(listener);

        shutdownOnInterrupt();
        communicator()->waitForShutdown();

        observable->removeListener(listener);
        return EXIT_SUCCESS;
    }
};

int main(int argc, char* argv[]) {
    MyApp app;
    return app.main(argc, argv);
}
