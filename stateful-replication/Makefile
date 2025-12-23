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

app-rm:
	-$(call ig_admin, application remove App)

app-deploy: app.xml app-rm
	$(call ig_admin, application add app.xml)

sentinel-status:
	docker exec stateful-replication-sentinel-1  redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster

run-client:
	counter/client.py --Ice.Config=locator.config "counter @ CounterGroup"

clean: down
	-$(RM) *~
