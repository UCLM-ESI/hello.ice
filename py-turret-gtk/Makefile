all:

clean:
	$(RM) *~ proxy.out

run-server: turret.py
	sudo ./server.py --Ice.Config=server.config | tee proxy.out

turret.py:
	git clone https://github.com/nickcoutsos/python-turret-host-controller
	ln -s python-turret-host-controller/turret.py .

run-client:
	./client.py '$(shell head -1 proxy.out)'
