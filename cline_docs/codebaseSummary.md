## Key Components

### Core Game Engine (galaxy_conquest.py)
- Main game loop controller
- State management system
- Event handling coordinator
- Resource initialization

### Game Systems
1. Star System Generator (star_system.py)
   - Procedural generation engine
   - System property management
   - Navigation control

2. Resource Manager (resources.py)
   - Resource tracking and distribution
   - Trading system implementation
   - Resource balance management

3. Background System (background.py)
   - Dynamic star field generation
   - Particle effect management
   - Screen update optimization

4. Menu System (menu.py)
   - User interface controller
   - Input handling
   - Menu state management

5. Persistence System (persistence.py)
   - Game state serialization
   - Save/load functionality
   - Data format conversion
   - Error handling

### View Layer
1. Startup View (views/startup.py)
   - Game initialization
   - New game/load game options
   - Initial menu interface with dynamic background
   - Smooth transition to galaxy view
   - State preservation

2. Galaxy View (views/galaxy.py)
   - Galaxy-wide navigation
   - Star system visualization
   - Resource overview display
   - Galaxy-specific menu controls

3. System View (views/system.py)
   - Individual system display
   - Planet orbit visualization
   - System resource management
   - System-specific menu controls

4. Planet View (views/planet.py)
   - Surface visualization
   - Resource extraction interface
   - Colony management system
   - Planet-specific menu controls

## Data Flow
1. Game Initialization
   - Display startup view
   - Process new game/load game selection
   - Load configuration from constants.py
   - Initialize resource system
   - Set up display and sprite groups
   - Load saved game state (if exists)

2. Game Loop
   - Process user input (view-specific menus)
   - Update game state (galaxy_conquest.py)
   - Update resource calculations (resources.py)
   - Render current view (views/*.py)
   - Update background effects (background.py)
   - Save game state (persistence.py)

3. Resource Management
   - Resource generation (star_system.py)
   - Resource collection (planet.py)
   - Resource trading (resources.py)
   - State persistence (persistence.py)

## Project Structure
```
galaxy-conquest/
├── galaxy_conquest.py     # Main entry point
├── game/                  # Core modules
│   ├── background.py      # Background effects
│   ├── constants.py       # Game constants
│   ├── enums.py          # Game enums
│   ├── menu.py           # Menu system
│   ├── persistence.py     # Save/load system
│   ├── properties.py      # Game properties
│   ├── resources.py       # Resource system
│   ├── star_system.py     # Star system gen
│   ├── transitions.py     # View transitions
│   └── views/            # View modules
│       ├── galaxy.py     # Galaxy view
│       ├── startup.py    # Startup view
│       ├── system.py     # System view
│       └── planet.py     # Planet view
├── tests/                 # Test suite
├── img/                   # Game assets
└── saves/                 # Save files
```

## External Dependencies
- Pygame: Graphics and game loop
- JSON: Save file format
- pytest: Testing framework
- Python standard library

## Recent Changes
- [2025-02-16] Implement view transition system with state preservation
- [2025-02-16] Create startup view with menu integration
- [2025-02-16] Add smooth transitions between views
- [2025-02-16] Add comprehensive test coverage for new modules
- [2025-02-16] Updated project roadmap with view system enhancement plan
- [2025-02-16] Extract save/load logic into persistence module
- [2025-02-16] Project structure established
- [2025-02-16] Core game modules created

## Code Style
- Following Google Python Style Guide
- 88 character line limit
- 4-space indentation
- Type hints and docstrings required

## Performance Considerations
- Using sprite groups for batch processing
- Implementing dirty rectangle updates
- Caching frequently used surfaces
- Resource pooling for particle effects
- Efficient collision detection

## Known Issues
- None documented yet

## Future Improvements
- Implement comprehensive resource trading
- Add more diverse planet types
- Enhance procedural generation
- Improve UI feedback system
