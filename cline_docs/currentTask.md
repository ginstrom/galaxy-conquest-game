## Current Objective
Fix the failing test in tests/test_star_system.py

## Context
After converting planets from dictionaries to a class, the test_planet_generation test was failing. The test expected planets to be dictionaries with keys that could be checked using the `in` operator, but the Planet class was missing the `__contains__` method.

## Status
✅ Fixed by adding a `__contains__` method to the Planet class to support the `in` operator.
- Method returns True for all valid planet attributes
- All tests now pass with 84% coverage
- Maintained backward compatibility with code expecting dictionary behavior

## Previous Tasks

### Convert planet object from dictionary to class
✅ Created Planet class in game/planet.py with:
- Attributes for name, type, size, resources, etc.
- Methods for dictionary conversion
- Dictionary-like access for compatibility
- Updated StarSystem, Game.load_game(), and persistence.py

### Refactor view navigation to use Game.to_state()
✅ Modified all view classes and Game methods to use to_state() for navigation:
- Centralized state transition logic
- Improved consistency in state management
- Reduced code duplication

### Fix "Resume Game" functionality
✅ Modified return_to_game method to:
- Always switch to System view when called from Galaxy View menu
- Auto-select first system if none selected
- Preserve original behavior for other states

### Refactor menu system to use pygame_gui
✅ Replaced custom menu rendering with pygame_gui components:
- Updated MenuItem to use UIButton
- Refactored Menu class to use UIPanel
- Added proper initialization and update methods
- Modified tests to work with new implementation

### Move notifications to dedicated class
✅ Created NotificationManager class in notifications.py:
- Moved notification code from Game class
- Added comprehensive tests
- Improved separation of concerns
