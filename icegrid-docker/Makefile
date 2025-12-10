#!/usr/bin/make -f

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef

up: down
	reset
	docker compose up -d --remove-orphans

down:
	docker compose down

logs:
	docker compose logs -f

rm-app:
	-$(call ig_admin, application remove PrinterApp)

add-app: up rm-app app-xml
	$(call ig_admin, application add app.xml)

client:
	../py/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter"

client-wko:
	../py/client.py --Ice.Config=locator.config printer1

clean: down
	-$(RM) *~
