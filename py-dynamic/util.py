# -*- mode: python; coding: utf-8 -*-


class InputStream:

    def __init__(self, data):
        self.data = data
        self.index = 0

    def readBool(self):
        retval = bool(self.data[self.index])
        self.index += 1
        return retval

    def readString(self):
        size = ord(self.data[self.index])
        self.index += 1

        retval = self.data[self.index:self.index+size]
        self.index += size
        return retval


class OutputStream:

    def __init__(self):
        self.data = ""

    def writeBool(self, data):
        self.data += chr(data)

    def writeString(self, data):
        self.data += chr(len(data))
        self.data += data

    def finished(self):
        return buffer(self.data)


