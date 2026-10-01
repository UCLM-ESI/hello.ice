all: Doc_pb2.py

%_pb2.py: %.proto
	python3 -m grpc_tools.protoc --python_out=. -I. $<

clean:
	$(RM) -r *.pyc __pycache__ *~ *_pb2.py
