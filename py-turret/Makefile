.PHONY: clean run-server run-client 

all:

clean:
	$(RM) *~ proxy.out

run-server: /etc/udev/rules.d/10-rocket-launcher.rules
	./Server.py --Ice.Config=Server.config | tee proxy.out

# KEEP IT: as reference if we need to access the original sources later
# turret.py:
# 	git clone https://github.com/nickcoutsos/python-turret-host-controller
# 	ln -s python-turret-host-controller/turret.py .

run-client:
	./Client.py '$(shell head -1 proxy.out)' up right left down

/etc/udev/rules.d/10-rocket-launcher.rules: 10-rocket-launcher.rules 
	sudo install $^ /etc/udev/rules.d/
