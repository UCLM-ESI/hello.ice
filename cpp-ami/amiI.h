#ifndef __amiI_h__
#define __amiI_h__

#include <ami.h>

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
