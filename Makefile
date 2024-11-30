#!make
define load_env
    $(eval include .env)
    $(eval export)
endef

up-postgres:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.postgres.yaml up -d
down-postgres:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.postgres.yaml down

up:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml up -d
down:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml down
rebuild:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml up -d --build
