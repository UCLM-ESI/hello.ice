#include <Freeze/Freeze.h>
#include <IceUtil/IceUtil.h>
#include <Hello.h>

using namespace std;
using namespace Ice;

class HelloI: public UCLM::HelloPersistent,
	      public IceUtil::AbstractMutexI<IceUtil::Mutex> {
  friend class HelloInitializer;
public:
  HelloI() { useCount = 0; }
  virtual void puts(const string& str, const Current& current) {
    cout << current.id.name << " (i=" << useCount << "): " << str << endl;
    useCount += 1;
  }
};

typedef IceUtil::Handle<HelloI> HelloIPtr;

class HelloFactory: public ObjectFactory {
public:
  virtual ObjectPtr create(const string& type) {
    return new HelloI();
  }

  virtual void destroy() {}
};

class HelloInitializer: public Freeze::ServantInitializer {
public:
  virtual void initialize(const ObjectAdapterPtr& oa,
			  const Identity& ident,
			  const string& str,
			  const ObjectPtr& obj) {
    HelloIPtr ptr = HelloIPtr::dynamicCast(obj);
    cout << ident.name << " Initial: " << ptr->useCount << endl;
  }
};

class Server: public Application {
public:
  virtual int run (int argc, char* argv[]) {
    shutdownOnInterrupt();
    communicator()->addObjectFactory(new HelloFactory(),
				     UCLM::HelloPersistent::ice_staticId());

    ObjectAdapterPtr adapter = communicator()->createObjectAdapter("OA");
    Freeze::EvictorPtr evictor =
      Freeze::createBackgroundSaveEvictor(adapter, "db", "hello",
					  new HelloInitializer());

    for (char i='0'; i<'5'; ++i) {
      char str[] = "Hello?";
      str[5] = i;
      Identity identity = communicator()->stringToIdentity(str);

      if (!evictor->hasObject(identity)) {
	ObjectPrx obj = evictor->add(new HelloI(), identity);
	cout << communicator()->proxyToString(obj) << endl;
      }
    }

    adapter->addServantLocator(evictor, "");
    adapter->activate();
    cout << "Ready" << endl;

    communicator()->waitForShutdown();
    cout << "Done" << endl;
    return 0;
  }
};

int main (int argc, char* argv[]) {
  Server* app = new Server();
  return app->main(argc, argv);
}
