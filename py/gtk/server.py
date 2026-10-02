#!/usr/bin/env -S python3 -u
"An Ice hello-world with GTK GUI"

import sys
import signal

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import Ice
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    def __init__(self, callback):
        self.on_message = callback

    def write(self, message, current=None):
        print(f"Client says: {message}")
        self.on_message(message)


class PrinterServerWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Printer Server")
        self.set_default_size(300, 100)
        self.set_resizable(False)

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.buffer = self.text_view.get_buffer()
        self.set_child(self.text_view)

    def add_message(self, message):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, message + '\n')


class PrinterServerApp(Gtk.Application):
    def __init__(self, ic):
        super().__init__(application_id='com.example.printerserver')
        self.ic = ic
        self.adapter = None
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = PrinterServerWindow(self)

            servant = PrinterI(self.window.add_message)
            self.adapter = self.ic.createObjectAdapter("PrinterAdapter")
            proxy = self.adapter.add(
                servant, self.ic.stringToIdentity("printer1"))

            print(proxy)
            self.window.add_message(str(proxy) + '\n----')

            self.adapter.activate()

        self.window.present()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: server.py --Ice.Config=<config-file>")

    with Ice.initialize(sys.argv) as communicator:
        app = PrinterServerApp(communicator)
        signal.signal(signal.SIGINT, lambda sig, frame: app.quit())
        app.run(None)
