#!/usr/bin/node
// -*- mode: js; coding: utf-8 -*-

(function() {

require("Ice");
require("./Printer");

var log = console.log;
var args = process.argv;
var exit = process.exit;
var ic;

// Define servant class
var PrinterI = function() {
    log("Printer created");
};

PrinterI.prototype = new Example.Printer();
PrinterI.prototype.constructor = PrinterI;

PrinterI.prototype.write = function(message, current) {
    log("write:", message);
}

// Launch Server
Ice.Promise.try(function() {
    // Create communicator
    ic = Ice.initialize();

    // Create object adapter
    return ic.createObjectAdapter("").then(function(adapter) {
	var proxy = adapter.addWithUUID(new PrinterI());
	log(proxy.toString());
    });

}).exception(function(ex) {
    log(ex.toString());

    // Stop communicator
    if (ic) {
	ic.destroy();
    }
});

}());
