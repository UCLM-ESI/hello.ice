#!/usr/bin/node
// -*- mode: js; coding: utf-8 -*-

(function() {

require("Ice");
require("./Printer");

var log = console.log;
var args = process.argv;
var exit = process.exit;
var ic;

Ice.Promise.try(function() {
    // Create communicator
    ic = Ice.initialize();
    if (! args[2]) {
	log("Usage: " + args[0] + " " + args[1] + " <proxy>");
	exit(1);
    }

    // Create and cast the given proxy
    var proxy = ic.stringToProxy(process.argv[2]);
    var printer = Example.PrinterPrx.uncheckedCast(proxy)
    log("Using proxy: '" + printer.toString() + "'");

    // Use the proxy
    printer.write('Hello World!');
    log("'Hello World!' sent.");

}).finally(function() {
    // Stop communicator
    if (ic) {
	return ic.destroy();
    }

}).exception(function(ex) {
    // Show what happend
    log(ex.toString());
    process.exit(1);

});

}());
