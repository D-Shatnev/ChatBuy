.PHONY: lint-check black-check isort-check flake8-check lint-fix black-fix isort-fix

SRC_DIRS=$(shell find . -path ./venv -prune -false -o -name '*.py')

lint-check: black-check isort-check flake8-check

black-check:
	@echo "Running Black for code style enforcement..."
	@black --check $(SRC_DIRS)

isort-check:
	@echo "Running isort to check imports..."
	@isort --check-only --profile black $(SRC_DIRS)

flake8-check:
	@echo "Running flake8 for linting..."
	@flake8 $(SRC_DIRS)

lint-fix: black-fix isort-fix

black-fix:
	@echo "Applying Black to format code..."
	@black $(SRC_DIRS)

isort-fix:
	@echo "Applying isort to organize imports..."
	@isort --profile black $(SRC_DIRS)