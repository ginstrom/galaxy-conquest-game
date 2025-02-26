## Current Objective
✅ Consolidate the duplicated code in game/views/infopanel.py lines 222-246 and 300-325

## Context
The `SystemViewInfoPanel` and `PlanetViewInfoPanel` classes in the infopanel.py file contained duplicated code for displaying planet details. This code duplication has been eliminated by extracting the common logic into a shared method in the parent `InfoPanel` class.

## Plan
1. Identify the duplicated code blocks in lines 222-246 and 300-325
2. Create a new method called `draw_planet_details()` in the parent `InfoPanel` class
3. Refactor both `SystemViewInfoPanel` and `PlanetViewInfoPanel` to use this new method
4. Ensure the behavior remains the same after refactoring
5. Run tests to verify all functionality works correctly

## Completed Steps
1. ✅ Identified duplicated code blocks for displaying planet details in `SystemViewInfoPanel` and `PlanetViewInfoPanel`
2. ✅ Created a new `draw_planet_details()` method in the parent `InfoPanel` class that encapsulates the common logic
3. ✅ Refactored `SystemViewInfoPanel` to use the new method for both hovered and selected planets
4. ✅ Refactored `PlanetViewInfoPanel` to use the new method for selected planets
5. ✅ Ran tests to verify all functionality works correctly (99% code coverage for infopanel.py)
6. ✅ Improved code maintainability and reduced duplication

## Next Steps
1. Consider adding more detailed planet information in the planet view
2. Explore adding interactive elements to the info panel
3. Improve visual styling of the info panel for better readability
