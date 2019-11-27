all: Doc_pb2.py

%_pb2.py: %.proto
	protoc --python_out=. $<

clean:
	$(RM) -r *.pyc __pycache__ *~ *_pb2.py
