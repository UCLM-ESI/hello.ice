#!/usr/bin/make -f

IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

up: down
	reset
	docker compose up --remove-orphans

down:
	docker compose down

show-nodes:
	$(IG_ADMIN) -e "node list"

add-app:
	$(IG_ADMIN) -e "application add app.xml"

rm-app:
	$(IG_ADMIN) -e "application remove PrinterApp"

clean: stop-grid
	-$(RM) *~
