#!/usr/bin/env -S python3 -u

import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import Ice
Ice.loadSlice('printer.ice')
import Example


class PrinterClientWindow(Gtk.ApplicationWindow):
    def __init__(self, app, ic, strproxy):
        super().__init__(application=app, title="Printer Client")
        self.set_default_size(200, 100)
        self.set_resizable(False)
        self.ic = ic
        self.printer = self.init_ice_proxy(strproxy)

        button = Gtk.Button(label="Click here")
        button.connect("clicked", self.on_button_clicked)
        self.set_child(button)

    def init_ice_proxy(self, strproxy):
        proxy = self.ic.stringToProxy(strproxy)
        printer = Example.PrinterPrx.checkedCast(proxy)
        if not printer:
            raise RuntimeError("Invalid proxy")
        return printer

    def on_button_clicked(self, button):
        self.printer.write("Hello World!")


class PrinterClientApp(Gtk.Application):
    def __init__(self, ic, strproxy):
        super().__init__(application_id='com.example.printerclient')
        self.ic = ic
        self.strproxy = strproxy
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = PrinterClientWindow(self, self.ic, self.strproxy)
        self.window.present()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: client.py <proxy-string>")

    with Ice.initialize(sys.argv) as communicator:
        app = PrinterClientApp(communicator, sys.argv[1])
        app.run(None)
