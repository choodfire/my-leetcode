run:
	uvicorn src.main:app --reload

check:
	ruff check && ruff format --check

migration:
	alembic revision --m="${NAME}" --autogenerate

migrate:
	alembic upgrade head
