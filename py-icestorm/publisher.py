#!/usr/bin/python

import sys
import Ice, IceStorm
Ice.loadSlice('./Printer.ice')
import Example


class Publisher(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print "property", key, "not set"
            return None

        print("Using IceStorm in: '%s'" % proxy)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print ': invalid proxy'
            return 2

        # Get topic
        try:
            topic = topic_mgr.retrieve("PrinterTopic")
        except IceStorm.NoSuchTopic:
            print "no such topic found, created"
            topic = topic_mgr.create("PrinterTopic")

        # Get publisher and call remote object method
        proxy = topic.getPublisher()

        prx = Example.PrinterPrx.uncheckedCast(proxy)

        print "publishing 10 'Hello World' events"
        for i in range(10):
            prx.write("Hello World!")

        return 0


sys.exit(Publisher().main(sys.argv))
