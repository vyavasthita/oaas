
NAME := Observability As a Service
REPO_URL := https://github.com/vyavasthita/oaas
COMPOSE_FILE ?= docker-compose.yaml
OBSERVABILITY_NETWORK_NAME ?= oaas-observability-net
K8S_DIR := ./k8s
K8S_NAMESPACE := oaas-observability
K8S_COMPONENTS := common loki opensearch-core opensearch tempo jaeger otel-collector alertmanager prometheus grafana
K8S_COMPONENTS_DELETE := grafana prometheus alertmanager otel-collector jaeger tempo opensearch opensearch-core loki common
GRAFANA_LOCAL_PORT ?= 8080
PORT_FORWARD_PID_FILE := .grafana-port-forward.pid
PORT_FORWARD_LOG := .grafana-port-forward.log
NAMESPACE_MANIFEST := $(K8S_DIR)/common/common_namespace.yaml
ALERTMANAGER_SECRET_TEMPLATE := $(K8S_DIR)/common/common_alertmanager_secret.yaml.tmpl
ALERTMANAGER_SECRET_FILE := $(K8S_DIR)/common/common_alertmanager_secret.yaml
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Welcome to $(NAME)!"
	@echo "Repository: $(REPO_URL)"
	@echo "Use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  all       clean the stack and bring it back up"
	@echo "  network   ensure the shared docker network exists"
	@echo "  otel      merge the OpenTelemetry Collector config"
	@echo "  up        build dependencies and start all services"
	@echo "  stop      stop running services"
	@echo "  down      remove services and orphans"
	@echo "  clean     tear down containers and anonymous volumes"
	@echo "  build     rebuild images without cache"
	@echo "  kup       apply the Kubernetes observability stack"
	@echo "  kdown     remove the Kubernetes observability stack"
	@echo "  ps        show container status"
	@echo "  logs      follow container logs"
	@echo "  status    alias for ps"
	@echo ""
	@echo "Choose one option!"

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
up: kdown stop network otel
	@echo "[up] docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans"
	@docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans


.PHONY: stop
stop:
	@echo "[stop] stopping containers (ignore errors if not running)"
	@docker compose -f $(COMPOSE_FILE) stop || true


.PHONY: down
down: stop-grafana-port-forward
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

# ===================== Kubernetes Helpers =====================
.PHONY: render-secrets
render-secrets:
	@value=$${OAAS_DISCORD_WEBHOOK_URL:-$$DISCORD_WEBHOOK_URL}; \
	 if [ -z "$$value" ]; then \
		echo "[secrets] Set OAAS_DISCORD_WEBHOOK_URL (or DISCORD_WEBHOOK_URL) before running make kup"; \
		exit 1; \
	 fi; \
	 encoded=$$(printf '%s' "$$value" | base64); \
	 sed "s|__DISCORD_WEBHOOK_URL_B64__|$$encoded|" $(ALERTMANAGER_SECRET_TEMPLATE) > $(ALERTMANAGER_SECRET_FILE); \
	 echo "[secrets] rendered $(ALERTMANAGER_SECRET_FILE) from template"

.PHONY: stop-grafana-port-forward
stop-grafana-port-forward:
	@if [ -f $(PORT_FORWARD_PID_FILE) ]; then \
		PID=$$(cat $(PORT_FORWARD_PID_FILE)); \
		if ps -p $$PID >/dev/null 2>&1; then \
			echo "[grafana] stopping existing port-forward (PID $$PID)"; \
			kill $$PID || true; \
		fi; \
		rm -f $(PORT_FORWARD_PID_FILE); \
	fi

.PHONY: grafana-port-forward
grafana-port-forward: stop-grafana-port-forward
	@echo "[grafana] starting port-forward on http://localhost:$(GRAFANA_LOCAL_PORT)"
	@nohup kubectl port-forward -n $(K8S_NAMESPACE) svc/grafana $(GRAFANA_LOCAL_PORT):3000 > $(PORT_FORWARD_LOG) 2>&1 & \
		echo $$! > $(PORT_FORWARD_PID_FILE); \
		echo "[grafana] logs: $(PORT_FORWARD_LOG)"

.PHONY: kup
kup: build down render-secrets
	@echo "[kup] deploying Kubernetes resources into namespace $(K8S_NAMESPACE)"
	@if [ -f $(NAMESPACE_MANIFEST) ]; then \
		echo "[kup] ensuring namespace $(K8S_NAMESPACE)"; \
		kubectl apply -f $(NAMESPACE_MANIFEST); \
	fi
	@for dir in $(K8S_COMPONENTS); do \
		if [ -d "$(K8S_DIR)/$$dir" ]; then \
			echo "[kup] kubectl apply -f $(K8S_DIR)/$$dir"; \
			kubectl apply -f $(K8S_DIR)/$$dir; \
		fi; \
	done
	@echo "[kup] waiting for deployments to become Available"
	@kubectl wait --namespace $(K8S_NAMESPACE) --for=condition=Available deployment --all --timeout=300s
	@$(MAKE) grafana-port-forward
	@echo "[kup] observability stack ready at http://localhost:$(GRAFANA_LOCAL_PORT)"

.PHONY: kdown
kdown: stop-grafana-port-forward
	@echo "[kdown] deleting Kubernetes resources from namespace $(K8S_NAMESPACE)"
	@for dir in $(K8S_COMPONENTS_DELETE); do \
		if [ -d "$(K8S_DIR)/$$dir" ]; then \
			echo "[kdown] kubectl delete -f $(K8S_DIR)/$$dir"; \
			kubectl delete -f $(K8S_DIR)/$$dir --ignore-not-found || true; \
		fi; \
	done
	@kubectl delete namespace $(K8S_NAMESPACE) --ignore-not-found || true
	@rm -f $(ALERTMANAGER_SECRET_FILE)