all: Doc_pb2.py

%_pb2.py: %.proto
	protoc --python_out=. $<
#	python3 -m grpc_tools.protoc -I. --python_out=. $<

clean:
	$(RM) -r *.pyc __pycache__ *~ *_pb2.py
