#include <Ice/Ice.h>
#include "Bool.h"

using namespace std;
using namespace Ice;
using namespace IBool;

class MyApp: public Application {
public:
    virtual int run(int argc, char* argv[]) {
        if (argc != 3) {
            cerr << "usage: " << appName() << " <bool-proxy> true|false" << endl;
            return EXIT_FAILURE;
        }

        ObjectPrx obj = communicator()->stringToProxy(argv[1]);
        RPrx r = RPrx::checkedCast(obj);
        cout << "previous value: " << r->get() << endl;
        WPrx w = WPrx::checkedCast(obj);
        Identity id;
        w->set(string("true") == argv[2], id);
        cout << "new value: " << r->get() << endl;
        return EXIT_SUCCESS;
    }
};

int main(int argc, char* argv[]) {
    MyApp app;
    return app.main(argc, argv);
}
