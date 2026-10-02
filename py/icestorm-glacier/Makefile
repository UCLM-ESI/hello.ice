#!/usr/bin/make -f

up: down
	docker compose up -d --build --remove-orphans

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f subscriber

publish:
	docker compose run --rm publisher

clean: down
	-$(RM) *~ */*~
