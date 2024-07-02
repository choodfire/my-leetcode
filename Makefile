run:
	uvicorn src.main:app --reload

check:
	ruff check && ruff format --check
