SHELL := /bin/bash

venv:
	python -m venv venv

.PHONY: setup-poetry
setup-poetry: ## Install poetry
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 -

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
	python3 -m app.main

.PHONY: build
build: ## Build the docker image
	docker build -t $(or $(image), fastapi-backend-template:local) .

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