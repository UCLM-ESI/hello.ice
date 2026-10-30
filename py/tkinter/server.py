#!/usr/bin/env -S python3 -u
"An Ice hello-world with Tkinter GUI"

import sys
import signal
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import Ice
Ice.loadSlice('printer.ice')
import Example


class PrinterI(Example.Printer):
    n = 0

    def __init__(self, callback):
        self.on_message = callback

    def write(self, message, current=None):
        message = f"{self.n}: {message}"
        print(message)
        self.on_message(message)
        self.n += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: server.py --Ice.Config=<config-file>")

    root = tk.Tk()
    root.title("Printer Server")
    text = ScrolledText(root, width=40, height=6, font=('Sans', 14),
                        wrap='word', padx=4, pady=4)
    text.pack(fill='both', expand=True)

    def add_message(message):
        text.insert('end', message + '\n')
        text.see('end')

    # run Ice dispatches in the Tk main loop (Tk is not thread-safe)
    init = Ice.InitializationData()
    init.dispatcher = lambda call, con: root.after(0, call)

    with Ice.initialize(sys.argv, init) as communicator:
        adapter = communicator.createObjectAdapter("PrinterAdapter")
        proxy = adapter.add(PrinterI(add_message),
                            communicator.stringToIdentity("printer1"))

        print(proxy)
        add_message(str(proxy) + '\n----')

        adapter.activate()
        signal.signal(signal.SIGINT, lambda sig, frame: root.quit())
        root.mainloop()
