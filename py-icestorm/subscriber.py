#!/usr/bin/python

import sys
import Ice, IceStorm
Ice.loadSlice('Hello.ice')
import Example


class HelloI(Example.Hello):
    def puts(self, s, current=None):
        print "Event received:", s


class Subscriber(Ice.Application):
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

        ic = self.communicator()
        adapter = ic.createObjectAdapter("HelloAdapter")
        servant = HelloI()

        proxy = adapter.addWithUUID(servant)

        try:
            topic = topic_mgr.retrieve("HelloTopic")
            qos = {}
            topic.subscribe(qos, proxy)

        except IceStorm.NoSuchTopic:
            print "no such topic found"
            return 3

        print 'Waiting events...', proxy

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        topic.unsubscribe(proxy)

        return 0


sys.exit(Subscriber().main(sys.argv))
