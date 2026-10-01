#include <Freeze/Freeze.h>
#include <IceUtil/IceUtil.h>
#include "counter.h"

using namespace std;
using namespace Ice;

class CounterI: public Counter::RWPersistent,
		public IceUtil::AbstractMutexI<IceUtil::Mutex> {
  friend class CounterInitializer;

public:
  CounterI() { status = 0; }
  virtual int get(const Current& current) {
    return status;
  }
  virtual void set(const int value, const Current& current) {
    status = value;
    cout << current.id.name << " value set to " << status << endl;
  }
  virtual void inc(const Current& current) {
    status++;
    cout << current.id.name << " value set to " << status << endl;
  }
};

typedef IceUtil::Handle<CounterI> CounterIPtr;

class CounterFactory: public ObjectFactory {
public:
  virtual ObjectPtr create(const string& type) {
    return new CounterI();
  }

  virtual void destroy() {}
};

class CounterInitializer: public Freeze::ServantInitializer {
public:
  virtual void initialize(
    const ObjectAdapterPtr& adapter, const Identity& identity,
    const string& str, const ObjectPtr& obj)
  {
    CounterIPtr ptr = CounterIPtr::dynamicCast(obj);
    cout << identity.name << " Initial: " << ptr->status << endl;
  }
};

class Server: public Application {
public:
  virtual int run (int argc, char* argv[]) {
    shutdownOnInterrupt();

    communicator()->addObjectFactory(new CounterFactory(),
				     Counter::RWPersistent::ice_staticId());

    _adapter = communicator()->createObjectAdapter("PrinterAdapter");
    _evictor = Freeze::createBackgroundSaveEvictor(_adapter, "db", "counters",
						  new CounterInitializer());

    for (char i='0'; i<'5'; ++i) {
      char str[] = "counter?";
      str[7] = i;
      ObjectPrx proxy = create_or_get_counter(str);
      cout << communicator()->proxyToString(proxy) << endl;
    }

    _adapter->addServantLocator(_evictor, "");
    _adapter->activate();

    cout << "-- Ready" << endl;
    communicator()->waitForShutdown();
    cout << "-- Done" << endl;
    return 0;
  }

  ObjectPrx create_or_get_counter(char* identity_str) {
    Identity identity = communicator()->stringToIdentity(identity_str);

    if (_evictor->hasObject(identity))
      return _adapter->createProxy(identity);

    cout << "-- New counter " << identity_str << endl;
    return _evictor->add(new CounterI(), identity);
  }

private:
  ObjectAdapterPtr _adapter;
  Freeze::EvictorPtr _evictor;
};

int main (int argc, char* argv[]) {
  Server app;
  return app.main(argc, argv);
}
