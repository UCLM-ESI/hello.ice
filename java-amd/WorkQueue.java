import java.util.concurrent.CompletableFuture;

public class WorkQueue extends Thread {
    class CallbackEntry {
        CompletableFuture<Long> future;
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
                    entry.future.complete(result);
                }
            }
        }

        // Throw exception for any outstanding requests.
	for(CallbackEntry p : _callbacks) {
            p.future.completeExceptionally(new Example.RequestCanceledException());
        }
    }

    public synchronized void
    add(CompletableFuture<Long> future, int value) {
        if (!_done) {
            // Add the work item.
            CallbackEntry entry = new CallbackEntry();
            entry.future = future;
            entry.value = value;

            if(_callbacks.size() == 0) {
                notify();
            }
            _callbacks.add(entry);
        }
	else {
            // Destroyed, throw exception.
            future.completeExceptionally(new Example.RequestCanceledException());
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
