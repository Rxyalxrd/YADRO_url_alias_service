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

install-dev:
	uv sync --all-groups

install-prod:
	uv sync 

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

makemigration:
	alembic revision --autogenerate -m "$(MSG)"

run:
	uvicorn app.main:app --reload
