COMPOSE_FILE=docker-compose.yaml

all: stop down clean up

stop:
	docker compose stop

clean:
	docker compose stop
	docker container prune -f
	docker image prune -f
	docker network prune -f

up:
	docker compose -f $(COMPOSE_FILE) up -d --build --remove-orphans

down:
	docker compose down

.PHONY: ps
ps:
	docker compose ps -a

.PHONY: logs
logs: ## show logs of containers
	docker compose -f $(COMPOSE_FILE) logs