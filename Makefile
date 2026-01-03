

COMPOSE_FILE=docker-compose.yaml
K8S_MANIFESTS_DIR=./k8s/manifests

.PHONY: all
all: stop down clean build up

.PHONY: stop
stop:
	echo "[stop] docker compose stop"
	docker compose stop

.PHONY: up
up: stop kstop otel
	echo "[up] docker compose -f $(COMPOSE_FILE) up -d --build  --remove-orphans"
	docker compose -f $(COMPOSE_FILE) up -d --build  --remove-orphans

.PHONY: down


down:
	echo "[down] docker-compose down --volumes"
	docker-compose down --volumes



COMPOSE_FILE=docker-compose.yaml
K8S_MANIFESTS_DIR=./k8s/manifests
K8S_MANIFESTS_DIR=./k8s/manifests

.PHONY: all
all: stop down clean build up

.PHONY: stop
stop:
	echo "[stop] docker compose stop"
	docker compose stop

.PHONY: clean

.PHONY: clean
clean:
	echo "[clean] Stop all running containers"
	docker compose stop
	echo "[clean] Remove all containers and volumes"
	docker compose down -v
	echo "[clean] Prune all stopped containers"
	docker container prune -f
	echo "[clean] Prune all unused images (including intermediate)"

.PHONY: backend-image-build

.PHONY: backend-image-build
backend-image-build:
	echo "[backend-image-build] Building backend Docker image from ./backend/Dockerfile as backend:latest"
	docker build -t backend:latest -f backend/Dockerfile .

.PHONY: build

.PHONY: build
build:
	echo "[build] docker-compose build --no-cache"
	docker-compose build --no-cache

.PHONY: up

.PHONY: up
up: stop kstop otel
	echo "[up] docker compose -f $(COMPOSE_FILE) up -d --build  --remove-orphans"
	docker compose -f $(COMPOSE_FILE) up -d --build  --remove-orphans

.PHONY: down

.PHONY: down
down:
	echo "[down] docker-compose down --volumes"
	docker-compose down --volumes

.PHONY: ps
ps:
	echo "[ps] docker compose ps -a"
	docker compose ps -a

.PHONY: otel
otel:
	echo "[otel] ./scripts/merge-otel-config.sh"
	./scripts/merge-otel-config.sh

.PHONY: logs
logs:
	echo "[logs] docker compose -f $(COMPOSE_FILE) logs"
	docker compose -f $(COMPOSE_FILE) logs

.PHONY: kup
kup: stop kstop backend-image-build
	echo "[kup] Applying Kubernetes manifests in $(K8S_MANIFESTS_DIR)"
	kubectl apply -f $(K8S_MANIFESTS_DIR)/namespace.yaml
	sh -c 'for f in $(K8S_MANIFESTS_DIR)/*.yaml; do if [ "$(basename $$f)" != "namespace.yaml" ]; then kubectl apply -f "$$f"; fi; done'
	echo "Waiting for backend pods to be ready..."
	kubectl wait --for=condition=Ready pod -l app=backend -n tic-tac-toe --timeout=60s || true

kdown:
	echo "[kdown] Deleting Kubernetes resources in $(K8S_MANIFESTS_DIR)"
	kubectl delete -f $(K8S_MANIFESTS_DIR)

.PHONY: kstop
kstop:
	echo "[kstop] Stopping all pods in tic-tac-toe namespace"
	kubectl delete pods --all -n tic-tac-toe

# ===================== Helm Commands =====================
.PHONY: hup
hup:
	echo "[hup] Installing/Upgrading Helm charts for monitoring stack"
	bash helm/monitoring/scripts/setup.sh

.PHONY: hclean
hclean:
	echo "[hclean] Cleaning Helm monitoring stack"
	bash helm/monitoring/scripts/clean.sh
# ========================== End ==========================