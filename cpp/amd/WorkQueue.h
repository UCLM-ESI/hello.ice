// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#ifndef WORK_QUEUE_H
#define WORK_QUEUE_H

#include <list>
#include <IceUtil/IceUtil.h>
#include "factorial.h"

class WorkQueue : public IceUtil::Thread {
public:
    WorkQueue();
    virtual void run();
    void add(const Example::AMD_Math_factorialPtr&, int);
    void destroy();

private:
    struct CallbackEntry {
        Example::AMD_Math_factorialPtr cb;
        int value;
    };

    IceUtil::Monitor<IceUtil::Mutex> _monitor;
    std::list<CallbackEntry> _callbacks;
    bool _done;
};

typedef IceUtil::Handle<WorkQueue> WorkQueuePtr;

#endif
