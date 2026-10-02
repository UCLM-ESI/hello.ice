#include <Ice/Ice.h>
#include <IceStorm/IceStorm.h>
#include <IceUtil/IceUtil.h>
#include "BoolObservable.h"
#include "BoolFactory.h"

using namespace std;
using namespace Ice;
using namespace IceUtil;
using namespace IceStorm;
using namespace IBool;

namespace IBool {

class RWObservableI : public RWObservable {
public:
    RWObservableI(const TopicManagerPrx& mgr) : _value(false) {
        _topic = mgr->create(generateUUID());
        _publisher = WPrx::uncheckedCast(_topic->getPublisher());
    }

    virtual bool get(const Current&) {
        Mutex::Lock lock(_mutex);
        return _value;
    }

    virtual void set(bool v, const Identity& id, const Current&) {
        {
            Mutex::Lock lock(_mutex);
            _value = v;
        }
        _publisher->set(v, id);
    }

    virtual void addListener(const WPrx& listener, const Current&) {
        try {
            _topic->subscribeAndGetPublisher(QoS(), listener);
        } catch (const AlreadySubscribed&) {
        }
    }

    virtual void removeListener(const WPrx& listener, const Current&) {
        _topic->unsubscribe(listener);
    }

    void destroyTopic() {
        _topic->destroy();
    }

private:
    Mutex _mutex;
    bool _value;
    TopicPrx _topic;
    WPrx _publisher;
};
typedef IceUtil::Handle<RWObservableI> RWObservableIPtr;


class RWRemoteFactoryI : public RWRemoteFactory {
public:
    RWRemoteFactoryI(const TopicManagerPrx& mgr) : _mgr(mgr) {}

    virtual ObjectPrx create(const Current& current) {
        return current.adapter->addWithUUID(new RWObservableI(_mgr));
    }

    virtual void destroy(const ObjectPrx& obj, const Current& current) {
        ObjectPtr servant = current.adapter->remove(obj->ice_getIdentity());
        RWObservableIPtr::dynamicCast(servant)->destroyTopic();
    }

private:
    TopicManagerPrx _mgr;
};

}


class Server: public Application {
public:
    virtual int run(int argc, char* argv[]) {
        string key = "IceStorm.TopicManager.Proxy";
        TopicManagerPrx mgr = TopicManagerPrx::checkedCast(
            communicator()->propertyToProxy(key));
        if (!mgr) {
            cerr << appName() << ": property " << key << " not set" << endl;
            return EXIT_FAILURE;
        }

        ObjectAdapterPtr oa = communicator()->createObjectAdapter("OA");
        ObjectPrx obj = oa->add(new RWRemoteFactoryI(mgr),
                                stringToIdentity("factory"));
        cout << communicator()->proxyToString(obj) << endl;

        oa->activate();
        shutdownOnInterrupt();
        communicator()->waitForShutdown();
        cout << "Done" << endl;
        return EXIT_SUCCESS;
    }
};

int main(int argc, char* argv[]) {
    Server app;
    return app.main(argc, argv);
}
