#!/usr/bin/env -S python3 -u

import sys
import Ice
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

Ice.loadSlice("armory.ice")
import Armory


class GUI:
    def __init__(self, app):
        self.app = app
        self.build_gui()

    def build_gui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        window = Gtk.Window(title="Turret Control")
        window.set_default_size(200, 100)
        window.add(vbox)

        buttons = {}
        for name in ["down", "up", "left", "right", "fire"]:
            button = Gtk.Button(label=name)
            buttons[name] = button

        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        vbox.pack_start(hbox1, True, True, 0)
        vbox.pack_start(hbox2, True, True, 0)
        vbox.pack_start(hbox3, True, True, 0)

        hbox1.pack_start(Gtk.Label(), True, True, 0)
        hbox1.pack_start(buttons["up"], True, True, 0)
        hbox1.pack_start(Gtk.Label(), True, True, 0)

        hbox2.pack_start(buttons["left"], True, True, 0)
        hbox2.pack_start(buttons["fire"], True, True, 0)
        hbox2.pack_start(buttons["right"], True, True, 0)

        hbox3.pack_start(Gtk.Label(), True, True, 0)
        hbox3.pack_start(buttons["down"], True, True, 0)
        hbox3.pack_start(Gtk.Label(), True, True, 0)

        buttons["down"].connect("pressed", lambda w: self.app.turret.down())
        buttons["up"].connect("pressed", lambda w: self.app.turret.up())
        buttons["left"].connect("pressed", lambda w: self.app.turret.left())
        buttons["right"].connect("pressed", lambda w: self.app.turret.right())
        buttons["fire"].connect("pressed", lambda w: self.app.turret.fire())

        for button in buttons.values():
            button.connect("released", self.on_button_released)

        window.show_all()
        window.connect("destroy", Gtk.main_quit)

    def on_button_released(self, wd):
        self.app.turret.stop()


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        self.turret = Armory.PanTiltPrx.checkedCast(proxy)
        if not self.turret:
            raise RuntimeError("Invalid proxy")

        Gtk.main()


app = Client()
gui = GUI(app)
sys.exit(app.main(sys.argv))
