# Galaxy Conquest Game Configuration

This directory contains configuration files that allow you to customize your Galaxy Conquest gaming experience without modifying the game's source code.

## Configuration Files

- `prefs.toml` - Player preferences and game settings

## How to Edit Configuration Files

### Basic Instructions

1. Open the configuration file (e.g., `prefs.toml`) in any text editor
2. Make your desired changes
3. Save the file
4. Restart the game for changes to take effect

### TOML Format

Configuration files use the TOML format (Tom's Obvious, Minimal Language), which is designed to be easy to read and write. Here are some basic rules:

- Lines starting with `#` are comments and don't affect the game
- Settings are organized in sections like `[game]` or `[galaxy]`
- Each setting follows the format: `setting_name = value`

### Available Settings

#### Debug Settings `[debug]`

```toml
[debug]
enabled = false  # Set to true to enable debug mode
```

#### Logging Settings `[logging]`

```toml
[logging]
level = "DEBUG"  # Log level: "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL"
format = "%(levelname)s - %(message)s"  # Format for log messages
```

#### Game Settings `[game]`

```toml
[game]
screen_width = 1024  # Game window width in pixels
screen_height = 768  # Game window height in pixels
fps = 30  # Frames per second (higher values are smoother but more CPU intensive)
```

#### Galaxy Settings `[galaxy]`

```toml
[galaxy]
num_star_systems = 15  # Number of star systems in the galaxy
num_background_stars = 300  # Number of background stars
num_nebulae = 5  # Number of nebulae
```

## Tips for Modifying Settings

- **Performance Issues**: If the game runs slowly, try reducing `fps`, `num_background_stars`, or `num_nebulae`
- **Larger Galaxy**: Increase `num_star_systems` for a more expansive game world
- **Screen Resolution**: Adjust `screen_width` and `screen_height` to match your display
- **Debugging**: Set `debug.enabled` to `true` and `logging.level` to `"DEBUG"` to help troubleshoot issues

## Restoring Default Settings

If you encounter problems after changing settings, you can:

1. Delete the modified configuration file
2. The game will automatically create a new file with default settings on the next launch

## Advanced Configuration

For more advanced configuration options, please refer to the full documentation in the `docs/configuration.md` file.
