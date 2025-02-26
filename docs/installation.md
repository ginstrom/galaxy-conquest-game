# Installation Guide

This document provides detailed instructions for installing and setting up the Galaxy Conquest game.

## System Requirements

- Python 3.9+
- Pygame 2.1.3
- Virtual environment recommended

## Basic Installation

1. Clone the repository:
```bash
git clone git@github.com:ginstrom/galaxy-conquest-game.git
cd galaxy-conquest-game
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development Setup

For development, install additional testing dependencies:
```bash
pip install -r requirements-dev.txt
```

These dependencies include:
- pytest
- pytest-cov
- pytest-mock
- flake8
- black

## Running the Game

### Using the Makefile (Recommended)

The project includes a Makefile to simplify installation and running the game:

```bash
# Set up the virtual environment and install all dependencies
make setup

# Run the game
make run
```

### Manual Method

If you prefer not to use the Makefile, you can run the game manually:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python galaxy_conquest.py
```

## Troubleshooting

### Common Issues

#### Pygame Installation Problems

If you encounter issues installing Pygame, try:

```bash
pip install --upgrade pip
pip install pygame==2.1.3
```

#### Display Issues

If you encounter display issues:
1. Ensure your graphics drivers are up to date
2. Try running the game with a different resolution by modifying the `config/prefs.toml` file

#### Virtual Environment Issues

If you have problems with the virtual environment:
1. Delete the `venv` directory
2. Reinstall the virtual environment using the commands above
