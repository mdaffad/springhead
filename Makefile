make_executable:
	chmod +x scripts/

install:
	poetry install --no-root

update_requirements:
	poetry export --without-hashes -o requirements/requirements.txt
	poetry export --without-hashes --dev -o requirements/requirements.dev.txt

ps:
	docker compose -f compose/docker-compose.yml --env-file env/.env ps

run_dev:
	docker compose -f compose/docker-compose.yml --env-file env/.env up --build

down_dev:
	docker compose -f compose/docker-compose.yml --env-file env/.env down -v --remove-orphans

# please run this command before start
# export $(cat env/.env.local | grep -v '#' | awk '/=/ {print $1}')
run_local: make_executable
	poetry run sh ./scripts/start-reload.sh
