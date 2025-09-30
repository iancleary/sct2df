help:
  just --list

# install package locally
dev:
  uv sync
  uv pip install '.'
  uv pip list
  uv lock

# install the module's dependencies
install:
  uv install

# run pre-commit hooks
pre-commit:
  uv run pre-commit run --all-files

precommit: pre-commit

# run ruff linter
lint:
  uv run ruff check .

# run ruff linter with 
fix:
  uv run ruff check . --fix

# run ruff formatter
format:
  uv run ruff format .

# run tests with coverage
test:
  uv run pytest tests
