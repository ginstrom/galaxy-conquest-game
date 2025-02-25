## Current Objective
Create a Makefile system with commands for running the game and running unit tests.

## Context
The project currently requires manual commands to run the game and execute tests. A Makefile will streamline these operations and provide a consistent interface for common development tasks.

## Plan
1. Create a Makefile in the project root with the following targets:
   - `run`: Activate the virtual environment and run the game
   - `test`: Activate the virtual environment and run the unit tests using pytest
   - `setup`: Create and activate the virtual environment and install dependencies

2. Ensure the Makefile works across different platforms (macOS, Linux)

3. Update documentation to reference the new Makefile commands

## Impact
- Simplified workflow for running the game and tests
- Consistent interface for common development tasks
- Improved developer experience
- Reduced friction for new contributors

## Next Steps
1. Create the Makefile with the necessary targets
2. Test the Makefile to ensure it works as expected
3. Update the documentation to reference the new Makefile commands
4. Update codebaseSummary.md to reflect the addition of the Makefile
