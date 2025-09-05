#!/usr/bin/env -S python3 -u

import sys
import Ice
import IceStorm

Ice.loadSlice('Printer.ice')
import Example  # noqa


class Publisher(Ice.Application):
    def run(self, args):
        printer = self.get_publisher("PrinterTopic")

        print("publishing 10 'Hello World' events")
        for i in range(10):
            printer.write("Hello World %s!" % i)

    def get_publisher(self, topic):
        topic = self.get_topic(topic)
        pub = topic.getPublisher()
        return Example.PrinterPrx.uncheckedCast(pub)

    def get_topic(self, topic_name):
        ic = self.communicator()
        mgr = ic.propertyToProxy("IceStorm.TopicManager.Proxy")
        mgr = IceStorm.TopicManagerPrx.checkedCast(mgr)

        try:
            return mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            return mgr.create(topic_name)


if __name__ == "__main__":
    Publisher().main(sys.argv)
