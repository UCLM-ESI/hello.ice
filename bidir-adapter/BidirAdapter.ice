// -*- mode: c++; coding: utf-8 -*-

#include <Ice/Identity.ice>

module Demo {

    interface BidirAdapter {
	Object* add(Object* proxy);
    };

};
