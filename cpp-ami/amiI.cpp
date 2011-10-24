
#include <iostream>
#include <amiI.h>

int
factorial_(int n) {
  if (n == 0)
	return 1;

  return n * factorial_(n-1);
}

::std::string int_to_str(int number) {
  ::std::stringstream ss;
   ss << number;
   return ss.str();
}

::std::string
UCLM::MathI::factorial(::Ice::Int value,
                       const Ice::Current& current) {
  return int_to_str(factorial_(value));
}
