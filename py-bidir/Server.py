#!/usr/bin/python -u
# -*- coding: utf-8; mode: python; -*-

import sys
import traceback
import threading
import Ice

Ice.loadSlice('Printer.ice')
Ice.loadSlice('-I{} Callback.ice'.format(Ice.getSliceDir()))
import Example


class PrinterCallbackI(Example.Callback, threading.Thread):
    def __init__(self, communicator):
        threading.Thread.__init__(self)
        self._broker = communicator
        self._destroy = False
        self._clients = []
        self._cond = threading.Condition()

    def destroy(self):
        self._cond.acquire()

        print("destroying callback sender")
        self._destroy = True

        try:
            self._cond.notify()
        finally:
            self._cond.release()

        self.join()

    def attach(self, ident, current=None):
        print("new printer '{}'".format(self._broker.identityToString(ident)))
        with self._cond:
            client = Example.PrinterPrx.uncheckedCast(current.con.createProxy(ident))
            self._clients.append(client)

    def run(self):
        num = 0

        while True:
            with self._cond:
                self._cond.wait(2)
                if self._destroy:
                    break

                clients = self._clients[:]

            if not clients:
                continue

            num = num + 1

            for p in clients:
                try:
                    p.write("text {}".format(num))
                except (Ice.CloseConnectionException, Ice.ConnectionLostException):
                    print("removing client '{}'".format(self._broker.identityToString(p.ice_getIdentity())))
                    traceback.print_exc()

                    with self._cond:
                        self._clients.remove(p)


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = PrinterCallbackI(broker)

        adapter = broker.createObjectAdapter("CallbackAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("callback"))
        print(proxy)

        adapter.activate()
        servant.start()

        try:
            self.communicator().waitForShutdown()
        finally:
            servant.destroy()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
