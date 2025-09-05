#include <Ice/Identity.ice>

module Example {
  interface Callback {
    void attach(Ice::Identity ident);
  };
};
