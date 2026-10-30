#!/usr/bin/env -S python3 -u
"An Ice hello-world with GTK GUI"

import sys
import signal
from time import sleep
import gi
import Ice

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    n = 0

    def __init__(self, callback):
        self.on_message = callback

    def write(self, message, current=None):
        message = f"{self.n}: {message}"
        print(message)
        self.on_message(message)
        self.n += 1


@Gtk.Template(filename='server.ui')
class PrinterServerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PrinterServerWindow'
    text_view = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app)
        for side in Gtk.TextWindowType.TOP, Gtk.TextWindowType.BOTTOM:
            self.text_view.set_gutter(side, Gtk.Box(height_request=4))
        self.buffer = self.text_view.get_buffer()
        self.buffer.create_tag('big', scale=1.3)
        self.end = self.buffer.create_mark(None, self.buffer.get_end_iter(), False)

    def add_message(self, message):
        self.buffer.insert_with_tags_by_name(
            self.buffer.get_end_iter(), message + '\n', 'big')
        self.text_view.scroll_mark_onscreen(self.end)


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

    init = Ice.InitializationData()
    init.dispatcher = lambda call, con: GLib.idle_add(call)

    with Ice.initialize(sys.argv, init) as communicator:
        app = PrinterServerApp(communicator)
        signal.signal(signal.SIGINT, lambda sig, frame: app.quit())
        app.run(None)
