#ifndef __PrinterI_h__
#define __PrinterI_h__

#include <printer.h>

namespace Example {

  class PrinterI : virtual public Printer {
  public:
    virtual void write(const ::std::string&,
		       const Ice::Current&);
  };
}

#endif
