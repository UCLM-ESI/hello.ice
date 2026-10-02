(function() {

class PrinterI extends Example.Printer {
    write(message, current) {
        writeLine("received callback: " + message);
    }
}

const communicator = Ice.initialize();
let connection;

async function start() {
    const hostname = document.location.hostname || "127.0.0.1";
    const proxy = communicator.stringToProxy(`callback:ws -h ${hostname} -p 7071`);

    const adapter = await communicator.createObjectAdapter("");
    const printer = adapter.addWithUUID(new PrinterI());
    const server = await Example.CallbackPrx.checkedCast(proxy);

    connection = proxy.ice_getCachedConnection();
    connection.setAdapter(adapter);
    await server.attach(printer.ice_getIdentity());
}

async function stop() {
    // The server unregisters the client when it fails to invoke the bidir proxy
    await connection.close(Ice.ConnectionClose.Gracefully);
    writeLine("browser object connection closed.");
}

function writeLine(msg) {
    const output = document.getElementById("output");
    output.value += msg + "\n";
    output.scrollTop = output.scrollHeight;
}

function setRunning(running) {
    document.getElementById("start").disabled = running;
    document.getElementById("stop").disabled = !running;
}

document.getElementById("start").onclick = async () => {
    setRunning(true);
    try {
        await start();
    } catch (ex) {
        writeLine(ex.toString());
        setRunning(false);
    }
};

document.getElementById("stop").onclick = async () => {
    try {
        await stop();
    } catch (ex) {
        writeLine(ex.toString());
    }
    setRunning(false);
};

}());
