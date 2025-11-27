#!/usr/bin/make -f

IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

up:
	reset
	docker compose up --remove-orphans

down: rm-app
	docker compose down

show-nodes:
	$(IG_ADMIN) -e "node list"

add-app: rm-app
	$(IG_ADMIN) -e "application add app.xml"

rm-app:
	-$(IG_ADMIN) -e "application remove PrinterApp" 2> /dev/null

client:
	../py/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter"

sockets:
	reset
	@echo registry:
	docker compose exec registry bash -c "ss -lptn"
	docker compose exec registry bash -c "netstat -lptn"
	@echo node1:
	docker compose exec node1 bash -c "ss -lptn"
	docker compose exec node1 bash -c "netstat -lptn"


clean: down
	-$(RM) *~
