// -*- coding: utf-8; mode: c++; tab-width: 4 -*-

#include <Ice/Identity.ice>

module Example {
  interface Callback {
    void register(Ice::Identity ident);
  };
};
