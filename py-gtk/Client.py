#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example

import gtk


class GUI:
    def __init__(self, app):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(200, 100)
        button = gtk.Button("click here")
        window.add(button)
        window.show_all()
        button.connect('clicked', self.on_button_clicked)
        window.connect('destroy', gtk.main_quit)

    def on_button_clicked(self, wd):
        app.print_hello()


class Client (Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        self.printer = Example.PrinterPrx.checkedCast(proxy)
        if not self.printer:
            raise RuntimeError("Invalid proxy")

        gtk.main()

    def print_hello(self):
        self.printer.write("Hello World!")


app = Client()
gui = GUI(app)
sys.exit(app.main(sys.argv))
