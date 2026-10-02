#ifndef __FACTORIALI_H__
#define __FACTORIALI_H__

#include "factorial.h"
#include "WorkQueue.h"

namespace Example {

class MathI : virtual public Math {
public:
    MathI(const WorkQueuePtr&);
    void factorial_async(const Example::AMD_Math_factorialPtr& cb,
			 int value, const Ice::Current&);
private:
    WorkQueuePtr _workQueue;
};

}

#endif
