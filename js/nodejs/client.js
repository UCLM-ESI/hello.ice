// -*- mode: js; coding: utf-8 -*-

require("Ice");
require("./Printer");

var log = console.log;
var args = process.argv;
var exit = process.exit;

(function() {

    var ic = Ice.initialize();
    if (! args[2]) {
	print("Usage: " + args[0] + " " + args[1] + " <proxy>");
	exit(1);
    }

    var proxy = ic.stringToProxy(process.argv[2]);
    var printer = Example.PrinterPrx.uncheckedCast(proxy);
    log("Using proxy: '" + printer.toString() + "'");

    printer.write('Hello World!');
    log("'Hello World!' sent.");

    exit(0);
}());
