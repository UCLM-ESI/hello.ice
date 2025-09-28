#!/usr/bin/env -S python3 -u

import sys
import Ice

Ice.loadSlice('armory.ice')
import Armory  # noqa: E402


class Client(Ice.Application):
    def handle_command(self, cmd):
        commands = {
            "up": self.turret.up,
            "down": self.turret.down,
            "left": self.turret.left,
            "right": self.turret.right,
            "fire": self.turret.fire,
        }
        action = commands.get(cmd)
        if action:
            action()
        else:
            print(f"Unknown command: {cmd}")

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
