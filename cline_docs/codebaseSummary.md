## Project Structure
```
galaxy-conquest-game/
├── game/               # Game source code
│   ├── views/         # Game view components
│   ├── game.py        # Main Game class
│   ├── notifications.py # Notification system
│   ├── persistence.py # Game state saving/loading
│   ├── resources.py   # Resource management
│   ├── star_system.py # Star system logic
│   └── menu.py        # Menu system
├── tests/             # Test suite
├── docs/              # Detailed documentation
├── img/               # Game assets
├── Makefile           # Build system for common tasks
└── README.md          # Project overview
```

## Configuration Management
- TOML-based configuration system in `config/prefs.toml`
- Hierarchical configuration with sections for debug, logging, display, and galaxy settings
- Configuration precedence: Command-line args > prefs.toml > default settings

## Key Components

### Resource Management
- ResourceManager: Handles game assets and caching
- TextCache: Optimizes text rendering

### Game Views
- GalaxyView: Main galaxy map
- SystemView: Individual star system view
- PlanetView: Detailed planet information
- StartupView: Game initialization and menu
- InfoPanel: Base class for information panels

### Notification System
- NotificationManager: Handles temporary notifications
- Supports save notifications with extensibility for other types

### Persistence System
- persistence.py: Handles saving and loading game state
- Converts game objects to/from JSON-serializable format
- Supports Planet objects with proper serialization/deserialization

### Testing Infrastructure
- Mock objects for pygame components
- Dependency injection for hardware independence
- High test coverage (84%)

## Recent Changes
- [2025-03-02] Fixed bootstrap command by switching from pygame to pygame-ce to resolve compilation issues
- [2025-03-02] Added SDL2 installation check to the bootstrap command
- [2025-03-02] Updated installation documentation with SDL2 installation instructions
- [2025-03-02] Discovered that pygame-ce installs as "pygame" module and reverted import changes
- [2025-03-02] Added bootstrap command to the Makefile for setting up dependencies
- [2025-03-02] Created prefs.toml.example file as a template for new installations
- [2025-03-02] Updated installation documentation to recommend using the bootstrap command
- [2025-03-02] Updated the help target in the Makefile to include the bootstrap command
- [2025-03-02] Changed project configuration to use Poetry and Python 3.10
- [2025-03-02] Created pyproject.toml file with Poetry configuration
- [2025-03-02] Updated Makefile to use Poetry commands
- [2025-03-02] Updated installation documentation with Poetry instructions
- [2025-03-02] Updated techStack.md to reflect the new dependency management system
- [2025-03-02] Made debug console's _console_output text area scrollable
- [2025-03-02] Fixed auto-scrolling by using the scroll bar's bottom_limit attribute
- [2025-03-02] Added test_scroll command to test scrolling functionality
- [2025-03-01] Fixed failing test in test_persistence.py by adding default values for missing keys
- [2025-03-01] Updated test_save_and_load_game_state to handle both dictionary and list formats for resources
- [2025-03-01] Fixed tests in test_view_panel_integration.py by adding MockDebug class
- [2025-03-01] Updated MockGame class to include debug attribute
- [2025-03-01] Made Debug instance a member of Game class
- [2025-03-01] Updated view files to use Game's debug instance
- [2025-03-01] Modified hover_utils.py to accept Game instance parameter
- [2025-03-01] Added toggle_console method to Game class
- [2025-03-01] Added debug console to the top of the screen using pygame_gui
- [2025-03-01] Implemented console toggle with backtick key and hide with ESC key
- [2025-03-01] Added basic command processing in the debug console
- [2025-02-28] Fixed error on load: AttributeError: 'dict' object has no attribute 'orbit_number'
- [2025-02-28] Updated persistence.py to convert planet dictionaries to Planet objects when loading game state
- [2025-02-28] Improved resource handling in convert_planet_data to support both dictionary and list formats
- [2025-02-28] Fixed bug in hover_utils.py causing TypeError when hovering over planets with None coordinates
- [2025-02-28] Added null checks in is_within_circle function and SystemView methods
- [2025-02-28] Fixed tests in test_star_system.py to work with the new dictionary-based resource format
- [2025-02-28] Fixed tests in test_planet.py to work with the new dictionary-based resource format
- [2025-02-28] Changed resource handling from list of dictionaries to a dictionary format
- [2025-02-28] Modified generate_resources to include all resource types
- [2025-02-28] Improved planet resource generation using beta distribution
- [2025-02-28] Added `__contains__` method to Planet class to support the `in` operator
- [2025-02-28] Converted planet object from dictionary to class
- [2025-02-28] Refactored view navigation to use Game.to_state()
- [2025-02-28] Fixed "Resume Game" functionality in Galaxy View menu
- [2025-02-28] Refactored menu system to use pygame_gui
- [2025-02-28] Moved notifications to dedicated NotificationManager class
- [2025-02-27] Fixed tests in test_infopanel.py, test_planet.py, test_game.py
- [2025-02-27] Replaced custom-drawn info panel with pygame_gui elements
- [2025-02-27] Consolidated duplicated code in InfoPanel classes
- [2025-02-26] Enhanced PlanetViewInfoPanel to display system information
- [2025-02-26] Improved test coverage for Game class (77%)
- [2025-02-26] Moved Game class to dedicated module
- [2025-02-26] Enhanced test coverage reporting with HTML reports
- [2025-02-25] Unified hover handling for planets and systems
