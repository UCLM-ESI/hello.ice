#!/usr/bin/env -S python3 -u

import sys
import Ice
import Glacier2
import IceStorm
from pathlib import Path

Ice.loadSlice(str(Path(__file__).parent / 'printer.ice'))
import Example  # noqa


class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print("Event received: {0}".format(message))


def create_session(ic):
    router = Glacier2.RouterPrx.checkedCast(ic.getDefaultRouter())
    router.createSession("user", "passwd")

    # keep the session alive
    timeout = router.getACMTimeout()
    if timeout > 0:
        connection = router.ice_getCachedConnection()
        connection.setACM(timeout, Ice.Unset, Ice.ACMHeartbeat.HeartbeatAlways)

    return router


def get_topic(ic, topic_name):
    mgr = ic.propertyToProxy("IceStorm.TopicManager.Proxy")
    mgr = IceStorm.TopicManagerPrx.checkedCast(mgr)

    print("Using IS: '{}'".format(mgr))
    try:
        return mgr.retrieve(topic_name)
    except IceStorm.NoSuchTopic:
        return mgr.create(topic_name)


def main(ic):
    router = create_session(ic)

    # objects in this adapter are reachable through the router
    adapter = ic.createObjectAdapterWithRouter("Adapter", router)
    adapter.activate()

    # Glacier2 forwards callbacks to this client by the identity category
    oid = Ice.Identity("PrinterReceiver", router.getCategoryForClient())
    proxy = adapter.add(PrinterI(), oid)
    print("Subscribed proxy: '{}'".format(proxy))

    topic = get_topic(ic, "PrinterTopic")
    topic.subscribeAndGetPublisher({}, proxy)

    print("Ready, waiting events...")
    try:
        ic.waitForShutdown()
    finally:
        topic.unsubscribe(proxy)


if __name__ == "__main__":
    try:
        with Ice.initialize(sys.argv) as communicator:
            main(communicator)
    except KeyboardInterrupt:
        pass
