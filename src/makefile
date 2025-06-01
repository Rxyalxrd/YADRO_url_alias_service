MSG = ""

.PHONY: clean install install-prod migrate downgrade makemigration run


clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".mypy_cache" -type d -exec rm -r {} +

install:
	uv sync

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

makemigration:
	alembic revision --autogenerate -m "$(MSG)"

run:
	uvicorn app.main:app --reload
