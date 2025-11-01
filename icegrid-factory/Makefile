#!/usr/bin/make -f

IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

start: ./tmp/db/registry ./tmp/db/node1
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! ss -ltnH 2>/dev/null | grep -q ':4061'; do sleep 1; done

stop:
	$(IG_ADMIN) -e "node shutdown node1"
	@while ss -ltnH 2>/dev/null | grep -q ':4061'; do sleep 1; done

add-app: start app.xml
	$(IG_ADMIN) -e "application add app.xml"

rm-app:
	$(IG_ADMIN) -e "application remove App"

run-client:
	./client.py --Ice.Config=locator.config factory

./tmp/db/%:
	mkdir -p $@

clean:
	-@$(MAKE) stop
	$(RM) -r *~ ./tmp
	find . \( -name "*.out" -o -name "*.err" \) -exec rm {} \;
