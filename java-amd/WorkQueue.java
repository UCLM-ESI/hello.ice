// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

import Example.*;

public class WorkQueue extends Thread {
    class CallbackEntry {
        AMD_Math_factorial cb;
        int value;
    }

    public synchronized void run() {
        while(!_done) {
            if(_callbacks.size() == 0) {
                try {
                    wait();
                } catch(java.lang.InterruptedException ex) { }
            }

            if(_callbacks.size() != 0) {
                // Get next work item.
                CallbackEntry entry = (CallbackEntry)_callbacks.getFirst();
		long result = factorial_(entry.value);

                if(!_done) {
                    // send response.
                    _callbacks.removeFirst();
                    entry.cb.ice_response(result);
                }
            }
        }

        // Throw exception for any outstanding requests.
	for(CallbackEntry p : _callbacks) {
            p.cb.ice_exception(new RequestCanceledException());
        }
    }

    public synchronized void
    add(AMD_Math_factorial cb, int value) {
        if (!_done) {
            // Add the work item.
            CallbackEntry entry = new CallbackEntry();
            entry.cb = cb;
            entry.value = value;

            if(_callbacks.size() == 0) {
                notify();
            }
            _callbacks.add(entry);
        }
	else {
            // Destroyed, throw exception.
            cb.ice_exception(new RequestCanceledException());
        }
    }

    public synchronized void
	_destroy() { // Thread.destroy is deprecated.
        _done = true;
        notify();
    }

    private java.util.LinkedList<CallbackEntry> _callbacks =
	new java.util.LinkedList<CallbackEntry>();

    public long factorial_(int n) {
	if (n == 0)
	    return 1;

	return n * factorial_(n-1);
    }

    private boolean _done = false;
}
