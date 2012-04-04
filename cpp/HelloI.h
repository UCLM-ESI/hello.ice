#ifndef __HelloI_h__
#define __HelloI_h__

#include <Hello.h>

namespace Example {

  class HelloI : virtual public Hello {
  public:
    virtual void puts(const ::std::string&,
		      const Ice::Current&);
  };
}

#endif
