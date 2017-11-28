BidirAdapter = function(local_adapter, remote_adapter) {
    this.local_adapter = local_adapter;
    this.remote_adapter = remote_adapter;

    this.conn = remote_adapter.ice_getCachedConnection();
    this.conn.setAdapter(local_adapter);
};

BidirAdapter.prototype.addWithUUID = function(servant) {
    var prx = this.local_adapter.addWithUUID(servant);
    return this.remote_adapter.add(prx);
};

BidirAdapter.prototype.add = function(servant, oid) {
    var ic = this.local_adapter.getCommunicator();
    var prx = this.local_adapter.add(servant, broker.stringToIdentity(oid));
    return this.remote_adapter.add(prx);
};

BidirAdapter.prototype.getCommunicator = function() {
    return this.local_adapter.getCommunicator();
};

BidirAdapter.prototype.getConnection = function() {
    return this.conn;
};


createBidirAdapter = function(broker, strprx) {
    var retval = new Ice.Promise();

    broker.createObjectAdapter("")
	.then(on_adapter_ready)
	.exception(function(ex) { retval.fail(ex); });

    var adapter;
    function on_adapter_ready(adapter_) {
	adapter = adapter_;

	var remote_adapter = broker.stringToProxy(strprx);
	return Utils.BidirAdapterPrx.checkedCast(remote_adapter)
	    .then(on_remote_adapter_prx_ready);
    };

    function on_remote_adapter_prx_ready(remote_adapter) {
	var remote_adapter = new BidirAdapter(adapter, remote_adapter);
	return retval.succeed(remote_adapter);
    };

    return retval;
};
