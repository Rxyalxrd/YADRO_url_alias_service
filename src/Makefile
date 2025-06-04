MSG = ""

.PHONY:
	downgrade
	clean
	install-dev
	install-prod
	migrate
	makemigration
	run


clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".mypy_cache" -type d -exec rm -r {} +

install:
	poetry install --no-root

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

makemigration:
	poetry run alembic revision --autogenerate -m "$(MSG)"

run:
	poetry run uvicorn app.main:app --reload
