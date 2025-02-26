## Current Objective
Unify hover handling logic for planets and systems.

## Context
Previously, hover handling was implemented differently for planets in the system view and star systems in the galaxy view. The planet hover detection was in the `SystemView.update()` method, while the system hover detection was directly in the main game loop in `galaxy_conquest.py`. This inconsistency made the code harder to maintain and extend.

## Completed Tasks
1. Created a new `hover_utils.py` module with common hover detection functions:
   - `check_hover`: A generic function to check if the mouse is hovering over any object in a list
   - `is_within_circle`: A helper function to check if the mouse is within a circular object

2. Updated hover detection in the main game loop to use the common functions for system hover detection

3. Updated the `SystemView.update()` method to use the common functions for planet hover detection

4. Added an `update()` method to the `PlanetView` class for consistency with other views

5. Added an `update()` method to the `GalaxyView` class for consistency with other views

## Impact
- Unified hover handling across different game views
- Improved code maintainability and readability
- Made the codebase more consistent and easier to extend
- Reduced code duplication

## Next Steps
1. Update tests to verify the unified hover functionality works correctly
2. Consider refactoring the main game loop to delegate hover detection to each view's `update()` method
3. Explore adding hover effects (e.g., highlighting) to improve visual feedback
4. Update documentation to reflect the architectural changes
