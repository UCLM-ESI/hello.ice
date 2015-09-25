#include <string>
#include <iostream>
#include <Ice/Connection.h>
#include "CallbackI.h"


using namespace Example;
using namespace std;

CallbackI::CallbackI(const Ice::CommunicatorPtr& broker) :
  _broker(broker), _destroy(false) {}

void
CallbackI::destroy() {
  {
    IceUtil::Monitor<IceUtil::Mutex>::Lock lck(*this);

    cout << "destroying callback sender" << endl;
    _destroy = true;

    notify();
  }

  getThreadControl().join();
}


void
CallbackI::attach(const Ice::Identity& ident,
                              const Ice::Current& current) {

  IceUtil::Monitor<IceUtil::Mutex>::Lock lck(*this);


  cout << "new printer '" << _broker->identityToString(ident) << "'" <<
    endl;

  Example::PrinterPrx client = Example::PrinterPrx::uncheckedCast(
    current.con->createProxy(ident));
  _clients.insert(client);
}

void
CallbackI::run() {
  int num = 0;

  while(true) {
    set<PrinterPrx> clients;

    {
      IceUtil::Monitor<IceUtil::Mutex>::Lock lck(*this);
      timedWait(IceUtil::Time::seconds(2));

      if(_destroy)
        break;

      clients = _clients;
    }

    if(!clients.empty()) {
      ++num;

      for(set<PrinterPrx>::iterator p=clients.begin(); p!= clients.end(); ++p) {
        try {
          stringstream stream;
          stream << "text " << num;
          (*p)->write(stream.str());
        }

        catch(const Ice::Exception& ex) {
          cerr << "removing client '" << _broker->identityToString(
            (*p)->ice_getIdentity()) << "'" << endl;

          IceUtil::Monitor<IceUtil::Mutex>::Lock lck(*this);
          _clients.erase(*p);
        }
      }
    }
  }
}
