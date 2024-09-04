# clean project
clean:
	rm poetry.lock
	poetry env remove --all
	rm -rf .ruff_cache
	rm -rf deepfoot/__pycache__/

# install project
install:
	poetry install

# run linting checks and attempt to fix
lint:
	poetry run ruff check --fix

# format code
format:
	poetry run ruff format .

# run tests and open coverage report
test:
	poetry run pytest tests/ --cov=deepfoot --cov-report=html:.htmlcov && open .htmlcov/index.html

run:
	poetry run python3 deepfoot/main.py
