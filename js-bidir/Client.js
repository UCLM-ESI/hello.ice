(function() {

var PrinterPrx = Example.PrinterPrx;

var PrinterI = Ice.Class(Example.Printer, {
    write: function(message, current) {
        writeLine("received callback: " + message);
    },
});

var id = new Ice.InitializationData();
id.properties = Ice.createProperties();

var communicator = Ice.initialize(id);
var connection;

var start = function() {
    // Create a proxy to the sender object.
    var hostname = document.location.hostname || "127.0.0.1";
    var proxy = communicator.stringToProxy("callback:ws -p 10002 -h " + hostname);

    return communicator.createObjectAdapter("").then(on_adapter_ready);

    function on_adapter_ready(adapter) {
	var printer = adapter.addWithUUID(new PrinterI());
	return Example.CallbackPrx.checkedCast(proxy).then(on_server_ready);

	function on_server_ready(server) {
	    connection = proxy.ice_getCachedConnection();
	    connection.setAdapter(adapter);

	    return server.attach(printer.ice_getIdentity());
	};
    };
};

var stop = function() {
    // Close the connection, the server will unregister the client
    // when it tries to invoke on the bi-dir proxy.
    writeLine("browser object connection closed.");
    return connection.close(false);
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

var writeLine = function(msg) {
    $("#output").val($("#output").val() + msg + "\n");
    $("#output").scrollTop($("#output").get(0).scrollHeight);
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
