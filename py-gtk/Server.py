#!/usr/bin/python -u
# -*- coding: utf-8 -*-
"A ICE hello-world with GTK GUI"

import sys

import Ice
Ice.loadSlice('Printer.ice')
import Example

import gtk, gobject
gobject.threads_init()


class PrinterI(Example.Printer):
    def write(self, s, current=None):
        print "Client say: ", s
        gobject.idle_add(gui.textbuffer.insert_at_cursor, s + '\n')


class GUI:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(200, 100)
        textview = gtk.TextView()
        window.add(textview)
        window.show_all()
        window.connect('destroy', gtk.main_quit)
        self.textbuffer = textview.get_buffer()


class Server(Ice.Application):
    def run(self, argv):

        ic = self.communicator()
        servant = PrinterI()

        adapter = ic.createObjectAdapter("PrinterAdapter")
        proxy = adapter.add(servant, ic.stringToIdentity("printer1"))

        print proxy

        adapter.activate()
        self.callbackOnInterrupt()
        gtk.main()
        ic.shutdown()
        return 0

    def interruptCallback(self, args):
        gobject.idle_add(gtk.main_quit)


gui = GUI()
sys.exit(Server().main(sys.argv))
