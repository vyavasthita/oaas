all: stop down clean up

stop:
	docker compose stop

clean:
	docker compose stop
	docker container prune -f
	docker image prune -f
	docker network prune -f

up:
	docker compose up -d --build --remove-orphans

down:
	docker compose down

ps:
	docker compose ps -a
