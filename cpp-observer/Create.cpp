#include <Ice/Ice.h>
#include "BoolFactory.h"

using namespace std;
using namespace Ice;
using namespace IBool;

class MyApp: public Application {
public:
    virtual int run(int argc, char* argv[]) {
        if (argc != 2) {
            cerr << "usage: " << appName() << " <factory-proxy>" << endl;
            return EXIT_FAILURE;
        }

        ObjectPrx obj = communicator()->stringToProxy(argv[1]);
        RWRemoteFactoryPrx f = RWRemoteFactoryPrx::checkedCast(obj);
        cout << communicator()->proxyToString(f->create()) << endl;
        return EXIT_SUCCESS;
    }
};

int main(int argc, char* argv[]) {
    MyApp app;
    return app.main(argc, argv);
}
