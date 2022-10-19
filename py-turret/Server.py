#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

import Ice

try:
    import Armory

except ModuleNotFoundError:
    Ice.loadSlice('Armory.ice')
    import Armory

try:
    import turret

except ModuleNotFoundError:
    print("Error: cannot found 'turret' module")
    sys.exit(1)


class PanTiltI(Armory.PanTilt):
    def __init__(self):
        self.driver = turret.Turret()

    def down(self, current=None):
        self.driver.down()

    def up(self, current=None):
        self.driver.up()

    def left(self, current=None):
        self.driver.left()
 
    def right(self, current=None):
        self.driver.right()

    def stop(self, current=None):
        self.driver.stop()

    def fire(self, current=None):
        self.driver.fire()
        time.sleep(7)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        try:
            servant = PanTiltI()

        except ValueError:
            print("Error configuring servant (is the turret connected?)")
            return 1

        adapter = broker.createObjectAdapter("TurretAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("turret1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
