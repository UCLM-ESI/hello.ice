#include <factorialI.h>

long int
factorial_(int n) {
  if (n == 0)
    return 1;

  return n * factorial_(n-1);
}

::Ice::Long
Example::MathI::factorial(::Ice::Int value,
                          const Ice::Current& current)
{
  return factorial_(value);
}
