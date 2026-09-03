#!/usr/bin/make -f

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef

up: down
	reset
	docker compose up --watch --remove-orphans

down:
	docker compose down

logs:
	docker compose logs -f

app-rm:
	-$(call ig_admin, application remove PrinterApp)

app-deploy: up app-rm app.xml
	$(call ig_admin, application add app.xml)

run-client:
	../py/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter"

run-client-wko:
	../py/client.py --Ice.Config=locator.config printer1

clean: down
	-$(RM) *~
