#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('Armory.ice')
import Armory


class Client(Ice.Application):
    def handle_command(self, cmd):
        if cmd == "up":
            self.turret.up()
        elif cmd == "down":
            self.turret.down()
        elif cmd == "left":
            self.turret.left()
        elif cmd == "right":
            self.turret.right()
        elif cmd == "fire":
            self.turret.fire()

    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        self.turret = Armory.PanTiltPrx.checkedCast(proxy)
        if not self.turret:
            raise RuntimeError("Invalid proxy")

        for cmd in argv[2:]:
            self.handle_command(cmd)

        return 0


app = Client()
sys.exit(app.main(sys.argv))
