## Project Structure
```
galaxy-conquest-game/
├── game/               # Game source code
│   ├── views/         # Game view components
│   ├── game.py        # Main Game class
│   ├── notifications.py # Notification system
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

### Testing Infrastructure
- Mock objects for pygame components
- Dependency injection for hardware independence
- High test coverage (84%)

## Recent Changes
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
- [2025-02-25] Added Makefile system for common development tasks
