#!/usr/bin/php5 -d ice.slice=Printer.ice
<?php
require 'Ice.php';
require 'Printer.php';

$ic = null;
try {
    $ic = Ice_initialize();
    $base = $ic->stringToProxy($argv[1]);
    $printer = Example_PrinterPrxHelper::checkedCast($base);
    if(!$printer)
        throw new RuntimeException("Invalid proxy");

    $printer->write("Hello World!");
}
catch(Exception $ex) {
    echo $ex;
}

if ($ic) {
    // Clean up
    try {
        $ic->destroy();
    }
    catch(Exception $ex) {
        echo $ex;
    }
}
?>
