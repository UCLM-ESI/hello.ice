#!/usr/bin/env php
<?php
require_once 'Ice.php';
require_once 'printer.php';

if ($argc != 2) {
    fwrite(STDERR, "usage: {$argv[0]} <proxy>\n");
    exit(1);
}

$communicator = Ice\initialize($argv);
try {
    $proxy = $communicator->stringToProxy($argv[1]);
    $printer = Example\PrinterPrxHelper::checkedCast($proxy);
    if (!$printer) {
        throw new RuntimeException("Invalid proxy");
    }

    $printer->write("Hello World!");
} finally {
    $communicator->destroy();
}
