// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <iostream>
#include <HelloI.h>

void
UCLM::HelloI::puts(const ::std::string& str,
                   const Ice::Current& current)
{
  std::cout << str << std::endl;
}
