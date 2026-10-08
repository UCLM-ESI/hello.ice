#!/bin/bash

reset
make -i clean
killall -9 icegridnode 2>/dev/null
sleep 0.5
make load-app
./client.py --Ice.Config=locator.config factory
