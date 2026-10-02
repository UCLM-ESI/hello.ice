// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#include <Ice/Ice.h>
#include "WorkQueue.h"

using namespace std;

Ice::Long factorial(int n) {
  if (n == 0)
    return 1;

  return n * factorial(n-1);
}


WorkQueue::WorkQueue() : _done(false) { }

void WorkQueue::run() {
  IceUtil::Monitor<IceUtil::Mutex>::Lock lock(_monitor);

  while (!_done) {
    if(_callbacks.size() == 0) {
      _monitor.wait();
    }

    if(_callbacks.size() != 0) {
      // Get next work item.
      CallbackEntry entry = _callbacks.front();

      // emulate a process that takes a significant period of
      // FIXME _monitor.timedWait(IceUtil::Time::milliSeconds(entry.value));
      Ice::Long result = factorial(entry.value);

      if (!_done) {
	// Print greeting and send response.
	_callbacks.pop_front();
	entry.cb->ice_response(result);
      }
    }
  }

  // Throw exception for any outstanding requests.
  list<CallbackEntry>::const_iterator p;
  for(p = _callbacks.begin(); p != _callbacks.end(); ++p) {
    (*p).cb->ice_exception(Example::RequestCanceledException());
  }
}

void WorkQueue::add(const Example::AMD_Math_factorialPtr& cb, int value) {
  IceUtil::Monitor<IceUtil::Mutex>::Lock lock(_monitor);

  if (_done) {
    cb->ice_exception(Example::RequestCanceledException());
    return;
  }

  // Add work item.
  CallbackEntry entry;
  entry.cb = cb;
  entry.value = value;

  if(_callbacks.size() == 0)
    _monitor.notify();

  _callbacks.push_back(entry);
}

void WorkQueue::destroy() {
    IceUtil::Monitor<IceUtil::Mutex>::Lock lock(_monitor);

    // Set done flag and notify.
    _done = true;
    _monitor.notify();
}
