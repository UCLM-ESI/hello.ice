#!/usr/bin/env -S python3 -u

import sys
import Ice
import IceStorm
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print(f"Event received: {message}")


def get_topic_manager(ic):
    key = 'IceStorm.TopicManager.Proxy'
    proxy = ic.propertyToProxy(key)
    if proxy is None:
        raise KeyError(f"property '{key}' not set")

    print("Using IceStorm in: '%s'" % key)
    retval = IceStorm.TopicManagerPrx.checkedCast(proxy)
    if not retval:
        raise ValueError("Invalid proxy for TopicManager")

    return retval


def main(ic):
    topic_mgr = get_topic_manager(ic)
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
    ic.waitForShutdown()

    topic.unsubscribe(subscriber)

    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as ic:
            sys.exit(main(ic))

    except KeyboardInterrupt:
        print("Shutting down subscriber...")
