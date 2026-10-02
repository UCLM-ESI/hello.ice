(function() {

const hostname = document.location.hostname || "127.0.0.1";
const initData = new Ice.InitializationData();
initData.properties = Ice.createProperties();
initData.properties.setProperty(
    "Ice.Default.Router", `Glacier2/router:ws -h ${hostname} -p 4064`);

const communicator = Ice.initialize(initData);
let session;

// All invocations go through the router, which requires a session
function getSession() {
    if (!session) {
        session = createSession().catch(ex => {
            session = undefined;
            throw ex;
        });
    }
    return session;
}

async function createSession() {
    const router = await Glacier2.RouterPrx.checkedCast(communicator.getDefaultRouter());
    // glacier.config uses the NullPermissionsVerifier: any user/password is valid
    await router.createSession("user", "password");

    // keep the session alive while the page is open
    const timeout = await router.getACMTimeout();
    const connection = router.ice_getCachedConnection();
    if (timeout > 0) {
        connection.setACM(timeout, undefined, Ice.ACMHeartbeat.HeartbeatAlways);
    }
    connection.setCloseCallback(() => {
        session = undefined;
        writeLine("router connection closed");
    });
    writeLine("session created");
}

async function send() {
    await getSession();
    const proxy = communicator.stringToProxy(document.getElementById("proxy").value);
    const printer = Example.PrinterPrx.uncheckedCast(proxy);
    const message = document.getElementById("message").value;
    await printer.write(message);
    writeLine("sent: " + message);
}

function writeLine(msg) {
    const output = document.getElementById("output");
    output.value += msg + "\n";
    output.scrollTop = output.scrollHeight;
}

document.getElementById("send").onclick = async () => {
    const button = document.getElementById("send");
    button.disabled = true;
    try {
        await send();
    } catch (ex) {
        writeLine(ex.toString());
    }
    button.disabled = false;
};

}());
