Galaxy Conquest
==============

A space exploration and conquest game built with Python and Pygame. Navigate through star systems, manage resources, and explore a procedurally generated galaxy.

## Features

- Procedurally generated star systems with unique characteristics
- Resource management and exploration mechanics
- Interactive menu system with keyboard and mouse support
- Dynamic background effects
- Modern UI with semi-transparent overlays

## Requirements

- Python 3.9+
- Pygame 2.1.3
- Virtual environment recommended

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd galaxy-conquest
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

## Project Structure

```
galaxy-conquest/
├── galaxy_conquest.py     # Main game entry point
├── game/                  # Game modules
│   ├── __init__.py
│   ├── background.py      # Background effects
│   ├── constants.py       # Game constants
│   ├── enums.py          # Game enums
│   ├── menu.py           # Menu system
│   ├── properties.py      # Star/Planet properties
│   ├── resources.py       # Resource management
│   └── star_system.py     # Star system generation
├── tests/                 # Test suite
│   ├── test_game.py
│   ├── test_menu.py
│   └── test_star_system.py
├── requirements.txt       # Production dependencies
└── requirements-dev.txt   # Development dependencies
```

## Running the Game

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python galaxy_conquest.py
```

## Testing

The project uses pytest for testing. Tests are located in the `tests/` directory.

Run the tests:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m pytest
```

Current test coverage:
- Overall coverage: 71%
- Full coverage for game constants and enums
- Menu system: 75% coverage
- Resource management: 68% coverage
- Star systems: 54% coverage

## Key Components

### Star Systems
- Procedurally generated star systems with different types (Main Sequence, Red Giant, White Dwarf, Blue Giant)
- Planet generation with various types and resources
- Collision detection for system placement

### Menu System
- Flexible menu creation with customizable items
- Keyboard and mouse input handling
- Semi-transparent overlay effects
- Resource-efficient text caching

### Resource Management
- Centralized resource manager for images and fonts
- Text caching system for improved performance
- Support for various planet and resource types

## Contributing

1. Install development dependencies
2. Write tests for new features
3. Ensure all tests pass
4. Maintain or improve code coverage

## License

[Add your license information here]