(function() {

class PrinterI extends Example.Printer {
    write(message, current) {
        writeLine("message received: " + message);
    }
}

const communicator = Ice.initialize();
let adapter;

async function start() {
    const hostname = document.location.hostname || "127.0.0.1";
    adapter = await createBidirAdapter(
        communicator, `bidir-adapter -t:ws -h ${hostname} -p 7071`);
    const printer = await adapter.addWithUUID(new PrinterI());
    document.getElementById("proxy").value = printer.toString();
}

async function stop() {
    // The BidirAdapter discards our proxy when it fails to forward an invocation
    await adapter.getConnection().close(Ice.ConnectionClose.Gracefully);
    document.getElementById("proxy").value = "";
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
