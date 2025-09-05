#!/usr/bin/env -S python3 -u

import sys
import Ice
import Glacier2
import IceStorm

Ice.loadSlice('printer.ice')
import Example  # noqa


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print("Event received: {0}".format(message))
        sys.stdout.flush()


class Subscriber(Glacier2.Application):
    def runWithSession(self, args):
        servant_prx = self.register_servant()
        print("Subscribed proxy: '{}'".format(servant_prx))
        self.subscribe_to_topic(servant_prx, topic="PrinterTopic")

        print("Ready, waiting events...")
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

    def createSession(self):
        return self.router().createSession("user", "passwd")

    def register_servant(self):
        ic = self.communicator()
        # adapter = ic.createObjectAdapter("PrinterAdapter")
        # adapter.activate()
        # return adapter.addWithUUID(PrinterI())

        # adapter = self.objectAdapter()

        adapter = ic.createObjectAdapterWithRouter("Adapter", self.router())
        adapter.activate()

        oid = self.createCallbackIdentity("PrinterReceiver")
        return adapter.add(PrinterI(), oid)

    def subscribe_to_topic(self, proxy, topic):
        topic = self.get_topic(topic)
        topic.subscribeAndGetPublisher({}, proxy)

    def get_topic(self, topic_name):
        ic = self.communicator()
        mgr = ic.propertyToProxy("IceStorm.TopicManager.Proxy")
        mgr = IceStorm.TopicManagerPrx.checkedCast(mgr)

        print("Using IS: '{}'".format(mgr))
        try:
            return mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            return mgr.create(topic_name)


if __name__ == "__main__":
    Subscriber().main(sys.argv)
