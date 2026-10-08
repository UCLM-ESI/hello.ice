import struct

# ice_invoke() sends and receives the parameters in an encapsulation: a header
# (total size as int, encoding major and minor version as bytes) and the data
ENCAPS_HEADER = '<iBB'
ENCAPS_HEADER_SIZE = struct.calcsize(ENCAPS_HEADER)
ENCODING_1_1 = (1, 1)


class InputStream:

    def __init__(self, data):
        size, major, minor = struct.unpack_from(ENCAPS_HEADER, data)
        self.data = bytes(data[ENCAPS_HEADER_SIZE:size])
        self.index = 0

    def readSize(self):
        size = self.data[self.index]
        self.index += 1

        if size == 255:
            size, = struct.unpack_from('<i', self.data, self.index)
            self.index += 4

        return size

    def readBool(self):
        retval = bool(self.data[self.index])
        self.index += 1
        return retval

    def readString(self):
        size = self.readSize()
        retval = self.data[self.index:self.index + size].decode('utf-8')
        self.index += size
        return retval


class OutputStream:

    def __init__(self):
        self.data = bytearray()

    def writeSize(self, size):
        if size < 255:
            self.data.append(size)
        else:
            self.data.append(255)
            self.data += struct.pack('<i', size)

    def writeBool(self, data):
        self.data.append(int(data))

    def writeString(self, data):
        encoded = data.encode('utf-8')
        self.writeSize(len(encoded))
        self.data += encoded

    def finished(self):
        header = struct.pack(ENCAPS_HEADER, ENCAPS_HEADER_SIZE + len(self.data),
                             *ENCODING_1_1)
        return header + bytes(self.data)
