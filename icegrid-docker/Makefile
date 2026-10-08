#!/usr/bin/make -f

up: down
	reset
	docker compose up --watch --remove-orphans

down:
	docker compose down

logs:
	docker compose logs -f

load-app:
	docker compose restart loader

run-client:
	../py/hello/client.py --Ice.Config=locator.config "printer1 @ PrinterServer1.PrinterAdapter"

run-client-wko:
	../py/hello/client.py --Ice.Config=locator.config printer1

clean: down
	-$(RM) *~
