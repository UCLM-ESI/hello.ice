#include <iostream>
#include "PrinterI.h"

void
Example::PrinterI::write(const ::std::string& message,
                      const Ice::Current& current) {
  num++;
  std::cout << num << ": " << message << std::endl;

}
