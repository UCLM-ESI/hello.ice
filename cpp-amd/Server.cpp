#include <Ice/Ice.h>
#include "factorialI.h"
#include "WorkQueue.h"

using namespace std;
using namespace Ice;

class AMDServer : public Application {
private:
    WorkQueuePtr _workQueue;

public:
  virtual int run(int, char*[]) {
    callbackOnInterrupt();

    _workQueue = new WorkQueue();
    Example::MathPtr servant = new Example::MathI(_workQueue);

    ObjectAdapterPtr adapter = \
      communicator()->createObjectAdapter("MathAdapter");
    ObjectPrx math = adapter->add(
      servant, communicator()->stringToIdentity("math1"));

    cout << communicator()->proxyToString(math) << endl;

    _workQueue->start();
    adapter->activate();
    communicator()->waitForShutdown();

    _workQueue->getThreadControl().join();

    return EXIT_SUCCESS;
  }

  virtual void interruptCallback(int) {
    _workQueue->destroy();
    communicator()->shutdown();
  }
};


int main(int argc, char* argv[]) {
    AMDServer app;
    return app.main(argc, argv);
}
