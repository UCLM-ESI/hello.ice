#!/usr/bin/env -S python3 -u

import sys
import Ice
import IceStorm
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'printer.ice'))
import Example  # noqa


def get_topic(ic, topic_name):
    mgr = ic.propertyToProxy("IceStorm.TopicManager.Proxy")
    mgr = IceStorm.TopicManagerPrx.checkedCast(mgr)

    try:
        return mgr.retrieve(topic_name)
    except IceStorm.NoSuchTopic:
        return mgr.create(topic_name)


def main(ic):
    topic = get_topic(ic, "PrinterTopic")
    printer = Example.PrinterPrx.uncheckedCast(topic.getPublisher())

    print("publishing 10 'Hello World' events")
    for i in range(10):
        printer.write("Hello World %s!" % i)


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        main(communicator)
