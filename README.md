Galaxy Conquest
==============

A space exploration and conquest game built with Python and Pygame. Navigate through star systems, manage resources, and explore a procedurally generated galaxy.

## Features

- Procedurally generated star systems with unique characteristics
- Resource management and exploration mechanics
- Interactive menu system with keyboard and mouse support
- Dynamic background effects
- Modern UI with semi-transparent overlays
- View-specific information panels
- Hardware-independent testing with mock objects
- High test coverage (>80%)

## Quick Start

1. Clone the repository and navigate to the project directory
2. Create and activate a virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Run the game with `python galaxy_conquest.py`

For detailed installation instructions, see [Installation Guide](docs/installation.md).

## Documentation

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Project Structure](docs/project_structure.md) - Overview of the codebase organization
- [Configuration Guide](docs/configuration.md) - How to configure the game
- [Testing Guide](docs/testing.md) - Testing approach and instructions
- [Contributing Guide](docs/contributing.md) - Guidelines for contributing
- [License Information](docs/license.md) - License details

## Development

For development, install additional testing dependencies:
```bash
pip install -r requirements-dev.txt
```

### Using the Makefile

The project includes a Makefile to simplify common development tasks:

```bash
# Set up the virtual environment and install dependencies
make setup

# Run the game
make run

# Run unit tests
make test

# Run tests with coverage report
make coverage

# Clean up generated files
make clean

# Show available commands
make help
```

Alternatively, you can run tests directly:
```bash
python -m pytest
```

## License

MIT License - See [License Information](docs/license.md) for details.
