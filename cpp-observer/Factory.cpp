#include "BoolPersistent.h"
#include "BoolFactory.h"
#include <Freeze/Freeze.h>
#include <IceUtil/IceUtil.h>
#include <IceStorm/IceStorm.h>
#include <Ice/Application.h>

using namespace std;
using namespace Ice;
using namespace IceUtil;
using namespace IceStorm;
using namespace Freeze;
using namespace IBool;

namespace IBool {

class RWPersistentI : public RWPersistent,
                      public AbstractMutexI<Mutex>
{
public:
    RWPersistentI(const TopicManagerPrx& mgr) : _mgr(mgr) {
        value = false;
        topic = 0;
    }

    virtual bool get(const Current&) {
        return value;
    }

    virtual void set(bool v,
                     const Identity& id,
                     const Current&) {
        value = v;
        getPublisher()->set(v, id);
    }

    virtual void addListener(const WPrx& obj,
                             const Current&) {
        getTopic()->subscribeAndGetPublisher(QoS(), obj);
    }

    virtual void removeListener(const WPrx& obj,
                                const Current&) {
        getTopic()->unsubscribe(obj);
    }

private:
    WPrx getPublisher() {
        if (_pub != 0) return _pub;
        return _pub = WPrx::uncheckedCast(getTopic()
                                          ->getPublisher());
    }

    TopicPrx getTopic() {
        if (topic != 0) return topic;
        return topic = _mgr->create(generateUUID());
    }

    WPrx _pub;
    TopicManagerPrx _mgr;
};

}
class RWObjectFactory: public ObjectFactory {
public:
    RWObjectFactory(const TopicManagerPrx& mgr) : _mgr(mgr) {}

    virtual ObjectPtr create(const string& type) {
        return new RWPersistentI(_mgr);
    }

    virtual void destroy() {}

private:
    TopicManagerPrx _mgr;
};
class RWInitializer: public Freeze::ServantInitializer {
public:
    virtual void initialize(const ObjectAdapterPtr& oa,
                            const Identity& ident,
                            const string& str,
                            const ObjectPtr& obj) {
    }
};


namespace IBool {

class RWRemoteFactoryI : public RWRemoteFactory {
public:
    RWRemoteFactoryI(const EvictorPtr& e,
                     const TopicManagerPrx& mgr) : _e(e), _mgr(mgr) {}

    virtual ObjectPrx create(const Current& c) {
        Ice::Identity identity = c.adapter->getCommunicator()->stringToIdentity(generateUUID());
	return _e->add(new RWPersistentI(_mgr), identity);
    }

    virtual void destroy(const ObjectPrx& obj, const Current&) {
        _e->remove(obj->ice_getIdentity());
    }

private:
    EvictorPtr _e;
    TopicManagerPrx _mgr;
};

}

class Server: public Application {
public:
    virtual int run (int argc, char* argv[]) {
        PropertiesPtr prop = communicator()->getProperties();
        string id = prop->getPropertyWithDefault("IceStorm.TopicManager.Proxy",
                                                 "IceStorm/TopicManager");

        ObjectPrx o = communicator()->stringToProxy(id);
        TopicManagerPrx mgr = TopicManagerPrx::checkedCast(o);
        communicator()->addObjectFactory(new RWObjectFactory(mgr),
                                         RWPersistent::ice_staticId());
        ObjectAdapterPtr oa = communicator()->createObjectAdapter("OA");
        Freeze::EvictorPtr e = createBackgroundSaveEvictor(
                oa, "db", "rw",
                new RWInitializer());
        oa->addServantLocator(e, "");
        oa->activate();

        ObjectPrx obj = oa->add(new RWRemoteFactoryI(e, mgr),
                                communicator()->stringToIdentity("factory"));
        cout << communicator()->proxyToString(obj) << endl;

        shutdownOnInterrupt();
        communicator()->waitForShutdown();
        cout << "Done" << endl;
        return 0;
    }
};

int main (int argc, char* argv[]) {
  Server* app = new Server();
  app->main(argc, argv);
}
