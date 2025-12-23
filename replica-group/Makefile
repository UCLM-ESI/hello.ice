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

app-rm:
	-$(call ig_admin, application remove App)

random round-robin ordered adaptive:
%: %.xml app-rm
	$(call ig_admin, application add $(@).xml)

round-client:
	../py-upper/client.py --Ice.Config=locator.config "tool1 @ ToolGroup"

clean: down
	-$(RM) *~
