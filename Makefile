SHELL := /bin/bash

venv:
	python -m venv venv

.PHONY: setup-poetry
setup-poetry: ## Install poetry
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.2 python3 -

.PHONY: pre-commit
pre-commit: ## Install pre-commit hooks
	pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## Run pre-commit hooks
	pre-commit run --all-files

.PHONY: install
install: ## Install main dependencies
	poetry install --sync

.PHONY: install-dev
install-dev: ## Install dependencies including dev dependencies such as test and docs
	poetry install --sync --with dev

.PHONY: ruff
ruff: ## Run ruff to check code style
	ruff check .

.PHONY: bandit
bandit: ## Run bandit to check for possible security issues
	bandit -r . -c pyproject.toml

.PHONY: mypy
mypy: ## Run mypy to check for type errors
	mypy . --config-file pyproject.toml

.PHONY: style
style: ## Run ruff, mypy and bandit to check code style
	ruff check . --fix
	mypy . --config-file pyproject.toml
	bandit -r . -c pyproject.toml

.PHONY: test
test: ## Run tests
	pytest .

.PHONY: test-coverage
test-coverage: ## Check test coverage
	pytest . --cov --cov-report term

.PHONY: run
run: ## Run the service locally
	bash entrypoint.sh

.PHONY: docker-build
docker-build: ## Build the docker image
	docker build -t $(or $(image), fastapi-backend-template:local) .

.PHONY: docker-run
docker-run: ## Run the docker image
	docker run -it -p $(APP_PORT):$(APP_PORT) \
	-e APP_HOST=$(APP_HOST) \
	-e APP_PORT=$(APP_PORT) \
	-e APP_TIMEOUT=$(APP_TIMEOUT) \
	-e APP_WORKERS=$(APP_WORKERS) \
	-e LOGGER_CONFIG_PATH=$(LOGGER_CONFIG_PATH) \
	-e DATABASE_PROTOCOL=$(DATABASE_PROTOCOL) \
 	-e DATABASE_DRIVER=$(DATABASE_DRIVER) \
    -e DATABASE_HOST=$(DATABASE_HOST) \
    -e DATABASE_PORT=$(DATABASE_PORT) \
    -e DATABASE_NAME=$(DATABASE_NAME) \
    -e DATABASE_USER=$(DATABASE_USER) \
    -e DATABASE_PASSWORD=$(DATABASE_PASSWORD) \
    -e AUTH_SECRET_KEY=$(AUTH_SECRET_KEY) \
	$(or $(image), fastapi-backend-template:local)

.PHONY: clean
clean: ## Clean up the project
	find . -type f -name "*.DS_Store" -ls -delete || true
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf || true
	find . | grep -E ".pytest_cache" | xargs rm -rf || true
	find . | grep -E ".mypy_cache" | xargs rm -rf || true
	find . | grep -E ".ruff_cache" | xargs rm -rf || true
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf || true
	find . | grep -E "dist" | xargs rm -rf || true
	rm -rf .coverage || true