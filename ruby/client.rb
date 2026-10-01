#!/usr/bin/ruby1.8

require 'Ice'
Ice.loadSlice('printer.ice')

ic = Ice.initialize(ARGV)
prx = ic.stringToProxy(ARGV[0])
printer = Example::PrinterPrx.checkedCast(prx)
printer.write("Hello, World!")
