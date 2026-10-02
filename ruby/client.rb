#!/usr/bin/env ruby

require 'Ice'
Ice::loadSlice(File.join(__dir__, 'printer.ice'))

Ice::initialize(ARGV) do |communicator|
  if ARGV.length != 1
    abort("usage: #{$0} <proxy>")
  end

  proxy = communicator.stringToProxy(ARGV[0])
  printer = Example::PrinterPrx::checkedCast(proxy)
  abort("invalid proxy") unless printer

  printer.write("Hello World!")
end
