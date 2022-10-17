
module Example {
    ["python:protobuf:Doc_pb2.Doc"] sequence<byte> Doc;

    interface DocPrinter {
        idempotent void write(Doc p);
    };
};

