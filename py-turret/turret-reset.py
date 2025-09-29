#!/usr/bin/env -S python3 -u

import turret


driver = turret.Turret()

driver.left(6)
driver.stop()

driver.right(2.8)
driver.stop()

driver.down(1)
driver.up(0.18)
driver.stop()
