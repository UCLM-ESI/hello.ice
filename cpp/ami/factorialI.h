#ifndef __factorialI_h__
#define __factorialI_h__

#include <factorial.h>

namespace Example
{

class MathI : virtual public Math
{
public:

    virtual ::Ice::Long factorial(::Ice::Int,
                                  const Ice::Current&);
};

}

#endif
