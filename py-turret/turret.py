"""
turret module provides access to the USB toy.

Code got and cleaned from https://github.com/nickcoutsos/python-turret-host-controller
"""

import logging
import time

import usb.core


DEFAULT_DURATION = 0.5

# Direction
DOWN  = 0x01
UP    = 0x02
LEFT  = 0x04
RIGHT = 0x08

# Action
FIRE = 0x10
STOP = 0x20

# States
MOVING = UP | DOWN | LEFT | RIGHT
FIRING = FIRE
STOPPED = STOP

logger = logging.getLogger('turret')
logger.setLevel(logging.DEBUG)


class Turret:
    def __init__(self, rockets=4):
        self._device = None
        self._rockets = rockets
        self._state = STOP
        self.connected = False
        self._connect()

    def __del__(self):
        if self.connected:
            self._disconnect()

    def _connect(self):
        logger.info('%r initiating connection to turret', self)
        self._device = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self._device is None:
            raise ValueError('Launcher not found.')

        if self._device.is_kernel_driver_active(0) is True:
            self._device.detach_kernel_driver(0)

        self._device.set_configuration()
        self._device.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        logger.info('%r connected successfully.', self)
        self.connected = True

    def _disconnect(self):
        self._device.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        try:
            self._device.attach_kernel_driver(0)
        except usb.core.USBError:
            pass
        
        logger.info('%r disconnected successfully.', self)

    def send(self, command, duration=None):
        self._state = command
        self._device.ctrl_transfer(0x21, 0x09, 0, 0,
            [0x02, command, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

        if duration is not None and command != STOP:
            time.sleep(duration)
            self.send(STOP)

    def up(self, duration=DEFAULT_DURATION):
        self.send(UP, duration)

    def down(self, duration=DEFAULT_DURATION):
        self.send(DOWN, duration)

    def left(self, duration=DEFAULT_DURATION):
        self.send(LEFT, duration)

    def right(self, duration=DEFAULT_DURATION):
        self.send(RIGHT, duration)

    def stop(self):
        self.send(STOP)

    def fire(self):
        self.send(FIRE)
