COMPOSE_FILE=docker-compose.yaml

all: stop down clean up

stop:
	docker compose stop

clean:
	docker compose stop
	docker container prune -f
	docker image prune -f
	docker network prune -f
	-docker volume rm tic-tac-toe_database_data
	-docker volume rm tic-tac-toe_grafana_data
	docker volume prune -f

	rm -rf /data/database/mysql/*

up: otel
	docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans

down:
	docker compose down

.PHONY: ps
ps:
	docker compose ps -a

.PHONY: logs
logs: ## show logs of containers
	docker compose -f $(COMPOSE_FILE) logs

.PHONY: helm
helm:
	bash helm/monitoring/scripts/setup.sh

helm-cl:
	bash helm/monitoring/scripts/clean.sh

.PHONY: restart
restart:
	@if [ -z "$(c)" ]; then \
		echo "Usage: make restart c=container1,container2,..."; \
		exit 1; \
	fi; \
	for container in $(subst ',', ,$(c)); do \
		echo "Restarting $$container..."; \
		docker compose restart $$container; \
	done

# Merge modular OpenTelemetry Collector YAML files into a single config
.PHONY: otel
otel:
	./scripts/merge-otel-config.sh