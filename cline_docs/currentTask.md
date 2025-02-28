## Current Objective
Update Game.draw_save_notification() in game/game.py to use Pygame GUI component

## Context
The `draw_save_notification()` method in the Game class currently uses direct pygame rendering to display a "Game Saved!" notification when the game is saved. This approach is inconsistent with the rest of the UI, which now uses pygame_gui components. The task is to refactor this method to use a pygame_gui UILabel component instead.

## Plan
1. Analyze the current implementation of `draw_save_notification()` - DONE
2. Understand how pygame_gui components are used in the codebase - DONE
3. Refactor the method to use a pygame_gui UILabel component - DONE
   - Create a UILabel when the notification should be shown
   - Remove the UILabel when the notification duration has passed
   - Ensure the notification appears in the same location and with similar styling
4. Update the test in `test_game_coverage.py` to verify the new implementation - DONE

## Current Status
The task has been completed successfully. The following changes were made:

1. Refactored `draw_save_notification()` method in `game/game.py` to use pygame_gui:
   - Replaced manual text rendering with a pygame_gui UILabel component
   - Added logic to create the label only if it doesn't already exist
   - Added logic to remove the label when the notification duration has passed
   - Positioned the label at the top center of the screen

2. Updated the test in `test_game_coverage.py` to verify the new implementation:
   - Mocked the pygame_gui.elements.UILabel class
   - Added assertions to verify that the label is created with the correct parameters
   - Added assertions to verify that the label is removed when the notification duration has passed
   - Ensured the test covers both the creation and removal of the notification

The changes maintain the same functionality while making the code more consistent with the rest of the UI implementation. The notification now appears in the same location and with similar styling, but uses the pygame_gui component system for better integration with the rest of the UI.
