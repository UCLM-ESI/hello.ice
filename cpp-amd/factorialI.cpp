#include "factorialI.h"
#include "WorkQueue.h"

using namespace Example;

MathI::MathI(const WorkQueuePtr& workQueue) :
  _workQueue(workQueue) { }

void MathI::factorial_async(const Example::AMD_Math_factorialPtr& cb,
                            int value, const Ice::Current&) {
  _workQueue->add(cb, value);
}
