#include <Ice/Identity.ice>

module IBool {
    interface R {
        idempotent bool get();
    };
    interface W {
        void set(bool v, Ice::Identity oid);
    };
};
