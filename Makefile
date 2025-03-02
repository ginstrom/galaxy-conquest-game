# Galaxy Conquest Game Makefile
# Provides commands for common development tasks

# Define the Poetry command
POETRY = poetry

# Default target
.PHONY: all
all: run

# Bootstrap the project - check requirements and set up everything
.PHONY: bootstrap
bootstrap:
	@echo "Bootstrapping Galaxy Conquest Game..."
	@echo "Checking Python version..."
	@if ! ($(shell which python3.10 || echo python3) -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10+ is required'" 2>/dev/null); then \
		echo "Python 3.10 or higher not found. Attempting to install..."; \
		$(MAKE) install-python; \
	else \
		echo "Python 3.10+ is already installed."; \
	fi
	@echo "Checking Poetry installation..."
	@command -v poetry >/dev/null 2>&1 || (echo "Poetry not found. Please install Poetry using the instructions in docs/installation.md" && exit 1)
	@echo "Checking SDL2 installation..."
	@command -v sdl2-config >/dev/null 2>&1 || (echo "SDL2 not found. Please install SDL2 using the instructions in docs/installation.md" && exit 1)
	@echo "Creating necessary directories..."
	@mkdir -p saves
	@echo "Installing dependencies..."
	$(POETRY) install
	@echo "Checking configuration..."
	@[ -f config/prefs.toml ] || cp config/prefs.toml.example config/prefs.toml 2>/dev/null || echo "Warning: Default configuration not found. You may need to create config/prefs.toml manually."
	@echo "Bootstrap complete! You can now run the game with 'make run'"

# Setup Poetry environment and install dependencies
.PHONY: setup
setup:
	$(POETRY) install

# Run the game
.PHONY: run
run:
	$(POETRY) run python galaxy_conquest.py

# Run unit tests
.PHONY: test
test:
	$(POETRY) run pytest

# Run tests with coverage report
.PHONY: coverage
coverage:
	$(POETRY) run pytest --cov=game --cov-report=term-missing --cov-report=html
	open htmlcov/index.html

# Clean up generated files and directories
.PHONY: clean
clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	$(POETRY) env remove --all

.PHONY: install-python
install-python:
	@echo "Detecting operating system..."
	@if [ "$(shell uname)" = "Darwin" ]; then \
		echo "macOS detected, installing Python 3.10 with Homebrew..."; \
		command -v brew >/dev/null 2>&1 || (echo "Homebrew not found. Installing Homebrew..." && /bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"); \
		brew install python@3.10; \
	elif [ "$(shell uname)" = "Linux" ]; then \
		echo "Linux detected, installing Python 3.10..."; \
		if command -v apt-get >/dev/null 2>&1; then \
			sudo apt-get update && sudo apt-get install -y software-properties-common && \
			sudo add-apt-repository -y ppa:deadsnakes/ppa && \
			sudo apt-get update && sudo apt-get install -y python3.10 python3.10-venv python3.10-dev; \
		elif command -v dnf >/dev/null 2>&1; then \
			sudo dnf install -y python3.10 python3.10-devel; \
		else \
			echo "Unsupported Linux distribution. Please install Python 3.10 manually."; \
			exit 1; \
		fi; \
	elif [ "$(shell uname -s | cut -c 1-5)" = "MINGW" ] || [ "$(shell uname -s | cut -c 1-4)" = "MSYS" ]; then \
		echo "Windows detected, please install Python 3.10 from https://www.python.org/downloads/"; \
		echo "After installation, make sure Python is added to your PATH."; \
		exit 1; \
	else \
		echo "Unsupported operating system. Please install Python 3.10 manually."; \
		exit 1; \
	fi

# Activate Poetry shell
.PHONY: shell
shell:
	$(POETRY) shell

# Help target
.PHONY: help
help:
	@echo "Galaxy Conquest Game Makefile"
	@echo "Available targets:"
	@echo "  bootstrap - Check requirements and set up everything for first-time use"
	@echo "  setup     - Install dependencies using Poetry"
	@echo "  run       - Run the game"
	@echo "  test      - Run unit tests"
	@echo "  coverage  - Run tests with coverage report (terminal and HTML) and open report in browser"
	@echo "  clean     - Clean up generated files and directories"
	@echo "  shell     - Activate Poetry shell"
	@echo "  help      - Show this help message"
