#!/usr/bin/make -f

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef

up:
	reset
	docker compose up -d --remove-orphans

down:
	docker compose down

build:
	docker compose build --no-cache

logs:
	docker compose logs -f

rm-app:
	-$(call ig_admin, application remove App)

load-app: app.xml rm-app
	$(call ig_admin, application add app.xml)

cluster-status:
	docker compose exec redis-node-1 redis-cli cluster nodes

run-client:
	counter/client.py --Ice.Config=locator.config "counter @ CounterGroup"

clean: down
	-$(RM) *~
