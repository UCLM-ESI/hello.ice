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
	-$(call ig_admin, application remove App)

load-app: rm-app
	$(call ig_admin, application add app.xml)

run-subscriber:
	../py/icestorm/subscriber.py --Ice.Config=subscriber.config

clean: down
	-$(RM) *~
