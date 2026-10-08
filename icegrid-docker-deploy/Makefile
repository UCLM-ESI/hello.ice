#!/usr/bin/make -f

define ig_admin
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "$(1)"
endef

start-grid: ssh/id_ed25519
	docker compose up -d --build --remove-orphans

stop-grid:
	docker compose down

show-logs:
	docker compose logs -f

show-nodes:
	$(call ig_admin, node list)

load-app:
	docker compose restart loader

deploy:
	ansible-playbook -i inventory.ini deploy.yml

start-servers:
	$(call ig_admin, server start PrinterServer1)
	$(call ig_admin, server start PrinterServer2)

show-server-out:
	$(call ig_admin, server show PrinterServer1 stdout)
	$(call ig_admin, server show PrinterServer2 stdout)

run-client:
	../py/hello/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter"
	../py/hello/client.py --Ice.Config=locator.config "printer1 @ PrinterServer2.PrinterAdapter"

ssh/id_ed25519:
	mkdir -p ssh
	ssh-keygen -q -t ed25519 -N '' -C icegrid-docker-deploy -f $@

clean: stop-grid
	-$(RM) -r ssh *~
