install:
	poetry install --no-root

update_requirements:
	poetry export --without-hashes -o requirements/requirements.txt
	poetry export --without-hashes --dev -o requirements/requirements.dev.txt

run_dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml --build up