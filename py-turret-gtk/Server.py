#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
import time

Ice.loadSlice('Armory.ice')
import Armory

sys.path.append('/home/david/repos/librocket')

import turret


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
        servant = PanTiltI()

        adapter = broker.createObjectAdapter("TurretAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("turret1"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
