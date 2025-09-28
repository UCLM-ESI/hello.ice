#!/usr/bin/env -S python3 -u

from __future__ import annotations

import logging
import random
import sys
import time
import unittest.mock as mock

import Ice

import turret

try:
    import Armory

except ModuleNotFoundError:
    Ice.loadSlice('armory.ice')
    import Armory




logging.basicConfig(level=logging.INFO)

class PanTiltI(Armory.PanTilt):
    def __init__(self, factory: TurretFactoryI):
        self.factory = factory
        try:
            self.driver = turret.Turret()
        except ValueError:
            self.driver = mock.MagicMock()
            logging.warning("Turret not connected, using mock driver")
    
    def self_delete(self, current: Ice.Current) -> None:
        """Remove this servant from the adapter."""
        current.adapter.remove(current.id)
        logging.info("Servant with identity %s has been removed", current.id)
        self.factory.renovate_token()

    def down(self, current: Ice.Current = None):
        self.driver.down()
        self.self_delete(current)

    def up(self, current: Ice.Current = None):
        self.driver.up()
        self.self_delete(current)

    def left(self, current: Ice.Current = None):
        self.driver.left()
        self.self_delete(current)

    def right(self, current: Ice.Current = None):
        self.driver.right()
        self.self_delete(current)

    def stop(self, current: Ice.Current = None):
        self.driver.stop()
        self.self_delete(current)

    def fire(self, current: Ice.Current = None):
        self.driver.fire()
        time.sleep(7)
        self.self_delete(current)


class TurretFactoryI(Armory.TurretFactory):
    def __init__(self):
        self.token = None
        self.proxy = None
        self.servant = PanTiltI(self)
        self.renovate_token()
    
    def renovate_token(self) -> None:
        """Generate a new token different from the previous one and print it."""
        while (new_token := random.randint(10, 99)) == self.token:
            new_token = random.randint(10, 99)
        
        logging.info("The new token is %d", new_token)
        self.token = new_token

    def getPanTilt(self, token: int, current: Ice.Current = None):
        # Here you would normally validate the token
        if token != self.token:
            raise Armory.InvalidToken("Wrong token")
    
        if self.proxy and current.adapter.find(self.proxy.ice_getIdentity()):
            raise Armory.InvalidToken("Token already used. Wait for a new one")
    
        self.proxy = Armory.PanTiltPrx.uncheckedCast(
            current.adapter.addWithUUID(self.servant)
        )
        return self.proxy


def main() -> int:
    """Entrypoint for the token server."""
    with Ice.initialize(sys.argv) as broker:
        servant = TurretFactoryI()
        adapter = broker.createObjectAdapter("TurretAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("factory"))
        logging.info("Proxy: %s", proxy)

        adapter.activate()
        try:
            broker.waitForShutdown()
        
        except KeyboardInterrupt:
            logging.info("Shutting down server")
            broker.shutdown()


if __name__ == "__main__":
    sys.exit(main())

