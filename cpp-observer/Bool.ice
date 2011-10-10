#include <Ice/Identity.ice>
module IBool {
    interface R {
        idempotent bool get();
    };
    interface W {
        ["freeze:write"]
        void set(bool v, Ice::Identity oid);
    };
};
