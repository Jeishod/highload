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

up-traefik:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.traefik.yaml up -d
down-traefik:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.traefik.yaml down

up:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml up -d
down:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml down
rebuild:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml up -d --build

create-tables:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml exec -it highload-backend poe create-tables

load-fixtures:
	$(call load_env)
	@docker compose -f .deployment/docker-compose.yaml exec -it highload-backend poe load-fixtures
