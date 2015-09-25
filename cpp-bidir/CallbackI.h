#ifndef PRINTERCALLBACKI_H
#define PRINTERCALLBACKI_H

#include <Ice/Communicator.h>
#include <Ice/Identity.h>
#include <IceUtil/IceUtil.h>
#include <Callback.h>
#include <Printer.h>

namespace Example {

  class CallbackI : virtual public Callback, public IceUtil::Thread,
                    public IceUtil::Monitor<IceUtil::Mutex> {
  public:
    CallbackI(const Ice::CommunicatorPtr&);
    void destroy();
    virtual void attach(const Ice::Identity&,
                        const Ice::Current&);
    virtual void run();

  private:
    const Ice::CommunicatorPtr _broker;
    bool _destroy;
    std::set<PrinterPrx> _clients;
  };

  typedef IceUtil::Handle<CallbackI> CallbackIPtr;
}



#endif
