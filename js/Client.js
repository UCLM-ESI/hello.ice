(function() {

var PrinterPrx = Example.PrinterPrx;

var PrinterI = Ice.Class(Example.Printer, {
    write: function(message, current) {
        writeLine("message received: " + message);
    },
});

start = function() {
    var idata = new Ice.InitializationData();
    broker = Ice.initialize(idata);

    var strprx = "bidir-adapter -t:ws -h " + location.hostname + " -p 9080";
    return createBidirAdapter(broker, strprx)
     	.then(on_adapter_ready);

    function on_adapter_ready(adapter_) {
	adapter = adapter_;
	var servant = new PrinterI();
	return adapter.addWithUUID(servant)
	    .then(on_printer_ready);
    };

    function on_printer_ready(printer) {
	writeProxy(printer);
    };
};

var stop = function() {
    // Close the connection, the server will unregister the client
    // when it tries to invoke on the bi-dir proxy.
    writeLine("browser object connection closed.");
    return adapter.getConnection().close(false);
};

// button click handlers
$("#start").click(function() {
    if (isConnected())
	return false;

    setState(State.Connecting);
    Ice.Promise.try(
	function() {
	    return start().then(function() {
                setState(State.Connected);
	    });
        }
    ).exception(
        function(ex) {
            $("#output").val(ex.toString());
            setState(State.Disconnected);
        }
    );
    return false;
});

$("#stop").click(function() {
    if (isDisconnected())
	return false;

    setState(State.Disconnecting);
    Ice.Promise.try(
        function() {
            return stop();
        }
    ).exception(
	function(ex) {
            $("#output").val(ex.toString());
        }
    ).finally(
        function() {
            setState(State.Disconnected);
        }
    );
    return false;
});

var writeProxy = function(proxy) {
    $("#proxy").val(proxy);
};

var writeLine = function(msg) {
    $("#output").val($("#output").val() + msg + "\n");
    $("#output").scrollTop($("#output").get(0).scrollHeight);
};

// Handle client state
var State = {
    Disconnected: 0,
    Connecting: 1,
    Connected: 2,
    Disconnecting: 3
};

var isConnected = function() {
    return state == State.Connected;
};

var isDisconnected = function() {
    return state == State.Disconnected;
};

var state;

var setState = function(s) {
    if (state == s) {
        return;
    }

    state = s;
    switch(s) {
    case State.Disconnected: {
        $("#start").removeClass("disabled");

        $("#progress").hide();
        $("body").removeClass("waiting");
        break;
    }
    case State.Connecting: {
        $("#output").val("");
        $("#start").addClass("disabled");

        $("#progress .message").text("Connecting...");
        $("#progress").show();
        $("body").addClass("waiting");
        break;
    }
    case State.Connected: {
        $("#stop").removeClass("disabled");

        $("#progress").hide();
        $("body").removeClass("waiting");
        break;
    }
    case State.Disconnecting: {
        $("#stop").addClass("disabled");

        $("#progress .message").text("Disconnecting...");
        $("#progress").show();
        $("body").addClass("waiting");
        break;
    }
    default: {
        break;
    }
    }
};

setState(State.Disconnected);

}());
