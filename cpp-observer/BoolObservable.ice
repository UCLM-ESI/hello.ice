#include "Bool.ice"

module IBool {
    interface Observable {
        idempotent void addListener(W* o);
        idempotent void removeListener(W* o);
    };

    interface RWObservable extends R, W, Observable {};
};
