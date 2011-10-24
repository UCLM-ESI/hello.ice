#ifndef __factorialI_h__
#define __factorialI_h__

#include <factorial.h>

namespace UCLM
{

class MathI : virtual public Math
{
public:

    virtual ::std::string factorial(::Ice::Int,
                                    const Ice::Current&);
};

}

#endif
