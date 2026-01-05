
NAME := Observability As a Service
REPO_URL := https://github.com/vyavasthita/oaas
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Welcome to $(NAME)!"
	@echo "Repository: $(REPO_URL)"
	@echo "Use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  all      clean the stack and bring it back up"
	@echo "  network  ensure the shared docker network exists"
	@echo "  otel     merge the OpenTelemetry Collector config"
	@echo "  up       build dependencies and start all services"
	@echo "  stop     stop running services"
	@echo "  down     remove services and orphans"
	@echo "  clean    tear down containers and anonymous volumes"
	@echo "  build    rebuild images without cache"
	@echo "  ps       show container status"
	@echo "  logs     follow container logs"
	@echo "  status   alias for ps"
	@echo ""
	@echo "Choose one option!"


COMPOSE_FILE ?= docker-compose.yaml
OBSERVABILITY_NETWORK_NAME ?= oaas-observability-net

.PHONY: all
all: clean up

.PHONY: network
network:
	@if ! docker network inspect $(OBSERVABILITY_NETWORK_NAME) >/dev/null 2>&1; then \
		echo "[network] creating docker network $(OBSERVABILITY_NETWORK_NAME)"; \
		docker network create $(OBSERVABILITY_NETWORK_NAME); \
	else \
		echo "[network] docker network $(OBSERVABILITY_NETWORK_NAME) already exists"; \
	fi

.PHONY: otel
otel:
	@echo "[otel] merging OpenTelemetry Collector config"
	@./scripts/merge-otel-config.sh

.PHONY: up
up: stop network otel
	@echo "[up] docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans"
	@docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans


.PHONY: stop
stop:
	@echo "[stop] stopping containers (ignore errors if not running)"
	@docker compose -f $(COMPOSE_FILE) stop || true


.PHONY: down
down:
	@echo "[down] removing containers and orphans (ignore errors if not running)"
	@docker compose -f $(COMPOSE_FILE) down --remove-orphans || true

.PHONY: clean
clean:
	@echo "[clean] tearing down containers, anonymous volumes, and orphans (ignore errors if not running)"
	@docker compose -f $(COMPOSE_FILE) down -v --remove-orphans || true
	@echo "[clean] pruning stopped containers"
	@docker container prune -f >/dev/null
	@echo "[clean] pruning unused images"
	@docker image prune -f >/dev/null || true

.PHONY: build
build:
	@echo "[build] rebuilding images without cache (ignore errors if not buildable)"
	@docker compose -f $(COMPOSE_FILE) build --no-cache || true

.PHONY: ps
ps:
	@docker compose -f $(COMPOSE_FILE) ps -a

.PHONY: logs
logs:
	@docker compose -f $(COMPOSE_FILE) logs -f

.PHONY: status
status: ps