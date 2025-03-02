# Installation Guide

This document provides detailed instructions for installing and setting up the Galaxy Conquest game.

## System Requirements

- Python 3.10+
- Poetry (dependency management)
- SDL2 (required for pygame-ce)
- pygame-ce 2.5.3

## Installing Dependencies

### Installing SDL2

SDL2 is required for pygame-ce to work properly. Here's how to install it:

#### On macOS:
```bash
brew install sdl2
```

#### On Ubuntu/Debian:
```bash
sudo apt-get install libsdl2-dev
```

#### On Windows:
Download and install the SDL2 development libraries from [the SDL website](https://www.libsdl.org/download-2.0.php).

### Installing Poetry

Before installing the game, you need to have Poetry installed on your system:

### On macOS/Linux:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### On Windows:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Verify the installation:
```bash
poetry --version
```

## Basic Installation

1. Clone the repository:
```bash
git clone git@github.com:ginstrom/galaxy-conquest-game.git
cd galaxy-conquest-game
```

2. Bootstrap the project (Recommended):
```bash
make bootstrap
```

This will:
- Check if Python 3.10+ is installed
- Check if Poetry is installed
- Create necessary directories
- Install all dependencies using Poetry
- Set up initial configuration

Alternatively, you can install dependencies manually:
```bash
poetry install
```

This will create a virtual environment and install all required dependencies, including development dependencies.

## Running the Game

### Using the Makefile (Recommended)

The project includes a Makefile to simplify running the game:

```bash
# Run the game
make run
```

### Using Poetry Directly

If you prefer not to use the Makefile, you can run the game directly with Poetry:

```bash
# Run the game
poetry run python galaxy_conquest.py

# Or activate the Poetry shell first
poetry shell
python galaxy_conquest.py
```

## Development Tasks

Poetry makes it easy to run development tasks:

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=game

# Generate HTML coverage report
poetry run pytest --cov=game --cov-report=html
```

## Troubleshooting

### Common Issues

#### Pygame-CE Installation Problems

If you encounter issues installing pygame-ce through Poetry, try:

```bash
# Make sure SDL2 is installed first
brew install sdl2  # On macOS
sudo apt-get install libsdl2-dev  # On Ubuntu/Debian

# Then try reinstalling pygame-ce
poetry add pygame-ce==2.5.3 --no-cache
```

If you're still having issues, you can check the [pygame-ce documentation](https://github.com/pygame-community/pygame-ce) for more troubleshooting tips.

#### Display Issues

If you encounter display issues:
1. Ensure your graphics drivers are up to date
2. Try running the game with a different resolution by modifying the `config/prefs.toml` file

#### Poetry Environment Issues

If you have problems with the Poetry environment:
1. Try removing the environment and reinstalling:
```bash
poetry env remove --all
poetry install
```

2. Update Poetry to the latest version:
```bash
poetry self update
```
