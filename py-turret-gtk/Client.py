#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('Armory.ice')
import Armory

import gtk


class GUI:
    def __init__(self, app):
        self.app = app
        self.build_gui()

    def build_gui(self):
        vbox = gtk.VBox()
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(200, 100)
        window.add(vbox)

        buttons = {}
        for name in ['down', 'up', 'left', 'right', 'fire']:
            button = gtk.Button(name)
            buttons[name] = button

        hbox1 = gtk.HBox(); vbox.add(hbox1)
        hbox2 = gtk.HBox(); vbox.add(hbox2)
        hbox3 = gtk.HBox(); vbox.add(hbox3)

        hbox1.add(gtk.Label())
        hbox1.add(buttons['up'])
        hbox1.add(gtk.Label())

        hbox2.add(buttons['left'])
        hbox2.add(buttons['fire'])
        hbox2.add(buttons['right'])

        hbox3.add(gtk.Label())
        hbox3.add(buttons['down'])
        hbox3.add(gtk.Label())

        buttons['down'].connect('pressed', lambda w: self.app.turret.down())
        buttons['up'].connect('pressed', lambda w: self.app.turret.up())
        buttons['left'].connect('pressed', lambda w: self.app.turret.left())
        buttons['right'].connect('pressed', lambda w: self.app.turret.right())
        buttons['fire'].connect('pressed', lambda w: self.app.turret.fire())

        for button in buttons.values():
            button.connect('released', self.on_button_released)

        window.show_all()
        window.connect('destroy', gtk.main_quit)

    def on_button_released(self, wd):
        self.app.turret.stop()


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        self.turret = Armory.PanTiltPrx.checkedCast(proxy)
        if not self.turret:
            raise RuntimeError("Invalid proxy")

        gtk.main()


app = Client()
gui = GUI(app)
sys.exit(app.main(sys.argv))
