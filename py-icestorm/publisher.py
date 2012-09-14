#!/usr/bin/python

import sys, Ice, IceStorm
Ice.loadSlice('./Hello.ice')
import Example


class Publisher(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
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

        # Get topic
        try:
            topic = topic_mgr.retrieve("HelloTopic")
        except IceStorm.NoSuchTopic:
            print "no such topic found, created"
            topic = topic_mgr.create("HelloTopic")

        # Get publisher and call remote object method
        base = topic.getPublisher()

        prx = Example.HelloPrx.uncheckedCast(base)

        print "publishing 10 'Hello World' events"
        for i in range(10):
            prx.puts("Hello world!")

        return 0


sys.exit(Publisher().main(sys.argv))
