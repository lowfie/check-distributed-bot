include .env

compose = sudo docker compose

up:
	$(compose) -f docker-compose.yaml up --build -d

logs-db:
	$(compose) logs -f db

logs-bot:
	$(compose) logs -f --no-log-prefix bot

logs-celery:
	docker compose logs -f --no-log-prefix celery

logs-scanner:
	$(compose) logs -f --no-log-prefix scanner

down:
	$(compose) down

shell:
	$(compose) exec bot poetry run python -m ptpython

shell-sql:
	docker compose exec db psql postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_SERVER):$(POSTGRES_PORT)/$(POSTGRES_DB)

shell-redis:
	docker compose exec redis redis-cli

revision:
	$(compose) exec bot poetry run alembic revision --autogenerate -m "update"

upgrade:
	$(compose) exec bot poetry run alembic upgrade +1

upgrade-head:
	$(compose) exec bot poetry run alembic upgrade head

downgrade:
	$(compose) exec bot poetry run alembic downgrade -1

clean-migrations:
	find . -path "*/alembic/versions/*.py" -not -path "*/venv/*" -not -path "*/__init__.py" -delete

restart: down up
