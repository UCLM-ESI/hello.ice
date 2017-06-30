#!/usr/bin/python3 -u
# -*- mode: python; coding: utf-8 -*-

import sys
import Ice
import IceStorm

Ice.loadSlice('Printer.ice')
import Example  # noqa


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print("Event received: {0}".format(message))
        sys.stdout.flush()


class Subscriber(Ice.Application):
    def run(self, args):
        servant_prx = self.register_servant()
        print("Subscribed proxy: '{}'".format(servant_prx))
        self.subscribe_to_topic(servant_prx, topic="PrinterTopic")

        print("Ready, waiting events...")
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

    def register_servant(self):
        ic = self.communicator()
        adapter = ic.createObjectAdapter("PrinterAdapter")
        adapter.activate()
        return adapter.addWithUUID(PrinterI())

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
