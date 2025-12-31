COMPOSE_FILE=docker-compose.yaml

all: stop down clean build up

stop:
	echo "[stop] docker compose stop"
	docker compose stop

clean:
	echo "[clean] Stop all running containers"
	docker compose stop

	echo "[clean] Remove all containers and volumes"
	docker compose down -v

	echo "[clean] Prune all stopped containers"
	docker container prune -f

	echo "[clean] Prune all unused images (including intermediate)"
	docker image prune -a -f

	echo "[clean] Prune all unused networks"
	docker network prune -f

	echo "[clean] Remove named database volume (if exists)"
	-docker volume rm tic-tac-toe_database_data

	echo "[clean] Remove named Grafana volume (if exists)"
	-docker volume rm tic-tac-toe_grafana_data

	echo "[clean] Prune all unused volumes"
	docker volume prune -f

	echo "[clean] Remove all database files"
	rm -rf ./data/database/mysql/*

	echo "[clean] Remove all Python build and cache artifacts"
	rm -rf backend/__pycache__ backend/.mypy_cache backend/.pytest_cache backend/dist backend/build

build:
	echo "[build] docker-compose build --no-cache"
	docker-compose build --no-cache

up: otel
	echo "[up] docker compose -f $(COMPOSE_FILE) up -d --build  --remove-orphans"
	docker compose -f $(COMPOSE_FILE) up -d --build  --remove-orphans

down:
	echo "[down] docker-compose down --volumes"
	docker-compose down --volumes

.PHONY: ps
ps:
	echo "[ps] docker compose ps -a"
	docker compose ps -a

# Merge modular OpenTelemetry Collector YAML files into a single config
.PHONY: otel
otel:
	echo "[otel] ./scripts/merge-otel-config.sh"
	./scripts/merge-otel-config.sh

.PHONY: logs
logs: ## show logs of containers
	echo "[logs] docker compose -f $(COMPOSE_FILE) logs"
	docker compose -f $(COMPOSE_FILE) logs

.PHONY: helm
helm:
	echo "[helm] bash helm/monitoring/scripts/setup.sh"
	bash helm/monitoring/scripts/setup.sh

helm-cl:
	echo "[helm-cl] bash helm/monitoring/scripts/clean.sh"
	bash helm/monitoring/scripts/clean.sh

.PHONY: restart
restart:
	@if [ -z "$(c)" ]; then \
		echo "Usage: make restart c=container1,container2,..."; \
		exit 1; \
	fi; \
	for container in $(subst ',', ,$(c)); do \
		echo "[restart] Restarting $$container..."; \
		docker compose restart $$container; \
	done