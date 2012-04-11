#include <iostream>
#include "HelloI.h"

void
Example::HelloI::puts(const ::std::string& message,
                      const Ice::Current& current) {
  std::cout << message << std::endl;
}
