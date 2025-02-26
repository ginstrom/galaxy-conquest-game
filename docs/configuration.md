# Configuration Guide

This document provides detailed information about configuring the Galaxy Conquest game.

## Configuration Files

The game uses TOML configuration files located in the `config/` directory. The main configuration file is `config/prefs.toml`, which allows you to override default settings without modifying the code.

## Configuration Structure

The configuration file is organized into sections:

```toml
[debug]
# Debug settings

[logging]
# Logging configuration

[display]
# Display settings

[galaxy]
# Galaxy generation settings
```

## Available Settings

### Debug Settings

```toml
[debug]
enabled = true  # Enable/disable debug mode
show_fps = true  # Show frames per second counter
```

### Logging Configuration

```toml
[logging]
level = "INFO"  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
file = "game.log"  # Log file path
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
```

### Display Settings

```toml
[display]
width = 1280  # Screen width in pixels
height = 720  # Screen height in pixels
fullscreen = false  # Enable/disable fullscreen mode
fps = 60  # Target frames per second
title = "Galaxy Conquest"  # Window title
```

### Galaxy Generation Settings

```toml
[galaxy]
size = 100  # Number of star systems in the galaxy
min_planets = 1  # Minimum number of planets per system
max_planets = 8  # Maximum number of planets per system
seed = 12345  # Random seed for procedural generation (use 0 for random seed)
```

## How Configuration Works

1. The game first loads default settings from `game/constants.py`.
2. It then looks for a `config/prefs.toml` file.
3. Any settings found in the configuration file override the default settings.
4. If a setting is not specified in the configuration file, the default value is used.

## Example Configuration

Here's an example of a complete configuration file:

```toml
[debug]
enabled = true
show_fps = true

[logging]
level = "INFO"
file = "game.log"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

[display]
width = 1280
height = 720
fullscreen = false
fps = 60
title = "Galaxy Conquest"

[galaxy]
size = 100
min_planets = 1
max_planets = 8
seed = 12345
```

## Modifying Configuration

To modify the configuration:

1. Open `config/prefs.toml` in a text editor.
2. Change the desired settings.
3. Save the file.
4. Restart the game for the changes to take effect.

For detailed instructions on modifying configuration files, see the README.md file in the `config/` directory.

## Configuration API

The game provides a configuration API in `game/config.py` that can be used to access configuration settings programmatically:

```python
from game.config import Config

# Get a configuration value
debug_enabled = Config.get("debug.enabled", default=False)

# Get a nested configuration section
display_config = Config.get_section("display")
```

## Advanced Configuration

### Environment Variables

Some configuration settings can be overridden using environment variables. Environment variables take precedence over settings in the configuration file.

For example:
```bash
GALAXY_CONQUEST_DEBUG=true python galaxy_conquest.py
```

### Command Line Arguments

The game also supports command line arguments for some settings:

```bash
python galaxy_conquest.py --debug --fullscreen
```

Run `python galaxy_conquest.py --help` to see all available command line options.
