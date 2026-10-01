#include "Bool.ice"
#include <IceStorm/IceStorm.ice>
module IBool {
    interface Observable {
        ["freeze:write"]
        idempotent void addListener(W* o);

        ["freeze:write"]
        idempotent void removeListener(W* o);
    };

    class RWPersistent implements R, W, Observable {
        bool value;
        IceStorm::Topic* topic;
    };
};
