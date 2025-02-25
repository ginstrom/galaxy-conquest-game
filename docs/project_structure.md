# Project Structure

This document provides a detailed overview of the Galaxy Conquest game project structure and file descriptions.

## Directory Structure

```
galaxy-conquest/
├── galaxy_conquest.py     # Main game entry point
├── config.toml            # Configuration file
├── game/                  # Game modules
│   ├── __init__.py
│   ├── background.py      # Background effects
│   ├── config.py          # Configuration management
│   ├── constants.py       # Game constants
│   ├── debug.py           # Debugging utilities
│   ├── enums.py           # Game enums
│   ├── logging_config.py  # Logging configuration
│   ├── menu.py            # Menu system
│   ├── persistence.py     # Save/load functionality
│   ├── properties.py      # Star/Planet properties
│   ├── resources.py       # Resource management
│   ├── star_system.py     # Star system generation
│   └── views/             # Game view components
│       ├── __init__.py
│       ├── galaxy.py      # Galaxy view
│       ├── infopanel.py   # Information panels
│       ├── planet.py      # Planet view
│       ├── startup.py     # Startup view
│       └── system.py      # System view
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py        # Test configuration
│   ├── mocks.py           # Mock objects for testing
│   ├── test_background.py
│   ├── test_config.py
│   ├── test_game.py
│   ├── test_infopanel.py
│   ├── test_menu.py
│   ├── test_persistence.py
│   ├── test_planet.py
│   ├── test_resources.py
│   ├── test_star_system.py
│   ├── test_startup.py
│   └── test_view_panel_integration.py
├── img/                   # Game assets
├── saves/                 # Save game files
├── docs/                  # Project documentation
├── cline_docs/            # Project management documentation
│   ├── codebaseSummary.md
│   ├── currentTask.md
│   ├── projectRoadmap.md
│   ├── techStack.md
│   └── testing_guidelines.md
├── Makefile               # Build system for common tasks
├── requirements.txt       # Production dependencies
└── requirements-dev.txt   # Development dependencies
```

## Key Components

### Main Game Files

- **galaxy_conquest.py**: The main entry point for the game. Initializes the game environment, sets up the display, and manages the game loop.
- **config.toml**: Configuration file for game settings. Can be modified to change game behavior without altering code.

### Game Module

The `game` directory contains the core game logic and components:

- **background.py**: Manages the dynamic background effects and star field rendering.
- **config.py**: Handles loading and parsing of configuration settings from config.toml.
- **constants.py**: Defines game-wide constants such as colors, sizes, and default values.
- **debug.py**: Contains debugging utilities for development and testing.
- **enums.py**: Defines enumeration types used throughout the game.
- **logging_config.py**: Configures the logging system for the game.
- **menu.py**: Implements the menu system with keyboard and mouse support.
- **persistence.py**: Handles saving and loading game state.
- **properties.py**: Defines properties for stars and planets.
- **resources.py**: Manages in-game resources and resource generation.
- **star_system.py**: Implements procedural generation of star systems.

### Views

The `game/views` directory contains the different view components of the game:

- **galaxy.py**: Implements the galaxy view, showing the overall map of star systems.
- **infopanel.py**: Implements information panels that display context-specific information.
- **planet.py**: Implements the planet view, showing detailed information about a selected planet.
- **startup.py**: Implements the startup view, including the main menu and game initialization.
- **system.py**: Implements the system view, showing a detailed view of a selected star system.

### Tests

The `tests` directory contains the test suite for the game:

- **conftest.py**: Contains pytest fixtures and configuration.
- **mocks.py**: Defines mock objects for hardware-independent testing.
- **test_*.py**: Individual test files for each game component.

### Assets

- **img/**: Contains game assets such as images and sprites.
- **saves/**: Directory for saved game files.

### Documentation

- **docs/**: Contains detailed project documentation.
- **cline_docs/**: Contains project management documentation.

### Build System

- **Makefile**: Provides a consistent interface for common development tasks:
  - `make setup`: Creates a virtual environment and installs dependencies
  - `make run`: Runs the game
  - `make test`: Runs the test suite
  - `make coverage`: Runs tests with coverage report
  - `make clean`: Cleans up generated files
  - `make help`: Shows available commands

### Dependencies

- **requirements.txt**: Lists production dependencies.
- **requirements-dev.txt**: Lists development dependencies.

## Module Relationships

- The main game loop in `galaxy_conquest.py` initializes and manages the different views.
- Views use components from the game module for functionality.
- The `infopanel.py` module provides context-specific information panels for each view.
- The `persistence.py` module interacts with the file system to save and load game state.
- The `config.py` module loads settings from `config.toml` and provides them to other modules.
