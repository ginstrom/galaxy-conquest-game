# Galaxy Conquest Game Makefile
# Provides commands for common development tasks

# Define the Python interpreter and virtual environment directory
PYTHON = python3
VENV_DIR = venv
VENV_BIN = $(VENV_DIR)/bin

# Default target
.PHONY: all
all: run

# Setup virtual environment and install dependencies
.PHONY: setup
setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_BIN)/pip install -r requirements.txt
	$(VENV_BIN)/pip install -r requirements-dev.txt

# Run the game
.PHONY: run
run:
	$(VENV_BIN)/python galaxy_conquest.py

# Run unit tests
.PHONY: test
test:
	$(VENV_BIN)/python -m pytest

# Run tests with coverage report
.PHONY: coverage
coverage:
	$(VENV_BIN)/python -m pytest --cov=game --cov-report=term-missing

# Clean up generated files and directories
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Help target
.PHONY: help
help:
	@echo "Galaxy Conquest Game Makefile"
	@echo "Available targets:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  run       - Run the game"
	@echo "  test      - Run unit tests"
	@echo "  coverage  - Run tests with coverage report"
	@echo "  clean     - Clean up generated files and directories"
	@echo "  help      - Show this help message"
