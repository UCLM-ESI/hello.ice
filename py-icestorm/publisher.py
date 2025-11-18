#!/usr/bin/env -S python3 -u

import sys
import Ice
import time
import IceStorm
Ice.loadSlice('./printer.ice')
import Example


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

    topic_name = "PrinterTopic"
    try:
        topic = topic_mgr.retrieve(topic_name)
    except IceStorm.NoSuchTopic:
        topic = topic_mgr.create(topic_name)

    publisher = topic.getPublisher()
    printer = Example.PrinterPrx.uncheckedCast(publisher)

    print("publishing 10 'Hello World' events")
    for i in range(10):
        printer.write("Hello World %s!" % i)
        time.sleep(1)

    return 0


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as ic:
            sys.exit(main(ic))

    except KeyboardInterrupt:
        print("Shutting down publisher")
