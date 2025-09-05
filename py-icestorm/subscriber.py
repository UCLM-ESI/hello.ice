#!/usr/bin/env -S python3 -u

import sys
import Ice
import IceStorm
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print("Event received: {0}".format(message))
        sys.stdout.flush()


class Subscriber(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid proxy")
            return 2

        ic = self.communicator()
        servant = PrinterI()
        adapter = ic.createObjectAdapter("PrinterAdapter")
        subscriber = adapter.addWithUUID(servant)

        topic_name = "PrinterTopic"
        qos = {}
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        print("Waiting events... '{}'".format(subscriber))

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0


sys.exit(Subscriber().main(sys.argv))
