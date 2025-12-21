#!/usr/bin/make -f

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef

up:
	reset
	docker compose up --scale redis-replica=2 --scale sentinel=3 -d --remove-orphans

down:
	docker compose down

build:
	docker compose build --no-cache

logs:
	docker compose logs -f

rm-app:
	-$(call ig_admin, application remove App)

add-app: app.xml rm-app
	$(call ig_admin, application add app.xml)

client:
	counter/client.py --Ice.Config=locator.config "counter @ CounterGroup"

clean: down
	-$(RM) *~
