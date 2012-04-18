#!/usr/bin/python

import sys, random
import Ice, IceStorm
Ice.loadSlice('Hello.ice')
import Example


class HelloI(Example.Hello):
    def puts(self, s, current=None):
        print "Event received:", s


class Subscriber(Ice.Application):

    def get_topic_manager(self):
        key = 'IceStormAdmin.TopicManager.Default'
        base = self.communicator().propertyToProxy(key)
        if base is None:
            print "property", key, "not set"
            return None

        print("Using IceStorm in: '%s'" % base)
        return IceStorm.TopicManagerPrx.checkedCast(base)

    def run(self, argv):

        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print ': invalid proxy'
            return 2

        ic = self.communicator()
        adapter = ic.createObjectAdapter("Hello.Subscriber")
        servant = HelloI()

        base = adapter.addWithUUID(servant)

        try:
            topic = topic_mgr.retrieve("HelloTopic")
            qos = {}
            topic.subscribe(qos, base)

        except IceStorm.NoSuchTopic:
            print "no such topic found"
            return 3

        print 'Waiting events...', base

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        topic.unsubscribe(base)

        return 0


sys.exit(Subscriber().main(sys.argv))
