// Register objects living in the browser in a remote BidirAdapter
// (see ../../bidir-adapter), so that any Ice client can invoke them.

class BidirAdapter {
    constructor(localAdapter, remoteAdapter) {
        this.localAdapter = localAdapter;
        this.remoteAdapter = remoteAdapter;

        this.connection = remoteAdapter.ice_getCachedConnection();
        this.connection.setAdapter(localAdapter);
    }

    addWithUUID(servant) {
        return this.remoteAdapter.add(this.localAdapter.addWithUUID(servant));
    }

    add(servant, name) {
        return this.remoteAdapter.add(
            this.localAdapter.add(servant, Ice.stringToIdentity(name)));
    }

    getConnection() {
        return this.connection;
    }
}

async function createBidirAdapter(communicator, strprx) {
    const localAdapter = await communicator.createObjectAdapter("");
    const remoteAdapter = await Utils.BidirAdapterPrx.checkedCast(
        communicator.stringToProxy(strprx));
    return new BidirAdapter(localAdapter, remoteAdapter);
}
