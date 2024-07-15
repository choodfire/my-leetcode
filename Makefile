run:
	uvicorn src.main:app --reload

check:
	ruff check && ruff format --check

fix:
	ruff format && ruff check --fix

migration:
	alembic revision --m="${NAME}" --autogenerate

migrate:
	alembic upgrade head
