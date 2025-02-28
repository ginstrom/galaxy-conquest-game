## Current Objective
Fix broken tests in tests/test_star_system.py

## Context
The resource handling in the game has been refactored to use a dictionary format instead of a list of dictionaries. The tests needed to be updated to match this new implementation. While tests in test_planet.py had been fixed, the tests in test_star_system.py still needed to be updated to work with the new resource format.

## Status
✅ Completed tasks:
- Fixed tests in test_planet.py to work with the new dictionary-based resource format
- Fixed tests in test_star_system.py to work with the new dictionary-based resource format:
  - Updated the import to include ResourceType from game.enums
  - Changed the assertion to check for a dictionary instead of a list for resources
  - Added assertions to verify that resource types are ResourceType enum values and amounts are integers between 0 and 100
- All tests now pass with the new resource format

## Next tasks:
- Continue updating any remaining tests that might still expect the old resource format
- Ensure all parts of the codebase are using the new resource format consistently

## Previous Tasks

### Refactor resource handling to use dictionary format
✅ Changed resource handling from list of dictionaries to a dictionary format:
- Removed the possible_resources value from PlanetProperties class
- Calculate all resource types for every planet type
- Changed generate_resources to return a dict with resource types as keys and values as values
- Modified Planet class and InfoPanel class to use this new dict format
- Updated tests to work with the new format

### Generate a planetary resource value for every resource type
✅ Modified generate_resources method to generate a value for every resource type:
- Now returns a resource value for every resource type in the ResourceType enum
- Uses the standard beta distribution for common resources (based on planet type)
- Uses a modified beta distribution with lower mean (0.1) for uncommon resources
- All tests pass with 84% code coverage

### Improve planet resource generation using beta distribution
✅ Updated resource generation in PlanetProperties class:
- Added numpy and scipy as dependencies in requirements.txt
- Added global variables MEAN (0.5) and VARIANCE (0.02) at the top of properties.py
- Calculated alpha and beta parameters for the beta distribution
- Modified generate_resources method to use beta distribution for resource values
- Resource values now range from 0 to 100 based on the beta distribution

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
