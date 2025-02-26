## Current Objective
Create a configuration system that can be edited by players

## Context
The game currently uses a single configuration file (`config.toml`) at the root of the project. We need to move this to a dedicated configuration directory and provide documentation for players on how to modify the configurations.

## Completed Steps
1. Created a new `config` directory in the project root
2. Moved the existing `config.toml` file to `config/prefs.toml`
3. Created a `config/README.md` file with instructions for players on how to modify configurations
4. Updated references to the configuration file in:
   - game/config.py - Updated the default configuration path
   - docs/configuration.md - Updated documentation about the configuration file location
   - docs/installation.md - Updated troubleshooting instructions
   - docs/project_structure.md - Updated project structure documentation
   - tests/test_config.py - Updated test cases to use the new file path
   - cline_docs/codebaseSummary.md - Updated references in the codebase summary
   - cline_docs/projectRoadmap.md - Added the completed task to the roadmap

## Impact
- More organized project structure with dedicated configuration directory
- Better user experience for players who want to customize their game
- Clear documentation on how to safely modify game settings
- Foundation for potentially adding more configuration files in the future
- All tests pass successfully with the new configuration file location
