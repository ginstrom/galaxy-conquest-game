import os
import toml
import argparse


def parse_arguments(args):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Galaxy Conquest Game')
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level'
    )
    # Add other configuration arguments that match config_loader.py
    parser.add_argument('--debug', type=bool, help='Enable/disable debug mode')
    parser.add_argument('--screen-width', type=int, help='Screen width')
    parser.add_argument('--screen-height', type=int, help='Screen height')
    parser.add_argument('--fps', type=int, help='Frames per second')
    parser.add_argument('--num-star-systems', type=int, help='Number of star systems')
    parser.add_argument('--num-background-stars', type=int, help='Number of background stars')
    parser.add_argument('--num-nebulae', type=int, help='Number of nebulae')
    return parser.parse_args()


def load_config(default_config_path='config/prefs.toml', args=None):
    """
    Load configuration from TOML file with optional command-line argument overrides.
    
    Args:
        default_config_path (str): Path to the default configuration file.
    
    Returns:
        dict: Merged configuration dictionary.
    """
    # Load default settings from settings module
    import settings

    # Default configuration dictionary
    config = {
        'debug': {
            'enabled': settings.DEBUG
        },
        'logging': {
            'level': settings.DEFAULT_LOG_LEVEL,
            'format': settings.LOG_FORMAT,
            'date_format': settings.LOG_DATE_FORMAT
        },
        'game': {
            'screen_width': settings.SCREEN_WIDTH,
            'screen_height': settings.SCREEN_HEIGHT,
            'fps': settings.FPS
        },
        'galaxy': {
            'num_star_systems': settings.NUM_STAR_SYSTEMS,
            'num_background_stars': settings.NUM_BACKGROUND_STARS,
            'num_nebulae': settings.NUM_NEBULAE
        }
    }

    # Try to load TOML configuration
    if os.path.exists(default_config_path):
        try:
            with open(default_config_path, 'r') as f:
                toml_config = toml.load(f)
                
            # Merge TOML config with default config
            for section, values in toml_config.items():
                if section in config:
                    config[section].update(values)
                else:
                    config[section] = values
        except Exception as e:
            print(f"Warning: Could not load configuration file: {e}")

    # Set up argument parser for command-line overrides
    parser = argparse.ArgumentParser(description='Galaxy Conquest Game Configuration')
    
    # Debug settings
    parser.add_argument('--debug', type=bool, help='Enable/disable debug mode')
    
    # Logging settings
    parser.add_argument('--log-level', type=str, help='Set logging level')
    parser.add_argument('--log-format', type=str, help='Set logging format')
    
    # Game settings
    parser.add_argument('--screen-width', type=int, help='Screen width')
    parser.add_argument('--screen-height', type=int, help='Screen height')
    parser.add_argument('--fps', type=int, help='Frames per second')
    
    # Galaxy settings
    parser.add_argument('--num-star-systems', type=int, help='Number of star systems')
    parser.add_argument('--num-background-stars', type=int, help='Number of background stars')
    parser.add_argument('--num-nebulae', type=int, help='Number of nebulae')

    # Parse command-line arguments
    args = parser.parse_args(args)

    # Override config with command-line arguments
    if args.debug is not None:
        config['debug']['enabled'] = args.debug
    
    if args.log_level:
        config['logging']['level'] = args.log_level
    if args.log_format:
        config['logging']['format'] = args.log_format
    
    if args.screen_width:
        config['game']['screen_width'] = args.screen_width
    if args.screen_height:
        config['game']['screen_height'] = args.screen_height
    if args.fps:
        config['game']['fps'] = args.fps
    
    if args.num_star_systems:
        config['galaxy']['num_star_systems'] = args.num_star_systems
    if args.num_background_stars:
        config['galaxy']['num_background_stars'] = args.num_background_stars
    if args.num_nebulae:
        config['galaxy']['num_nebulae'] = args.num_nebulae

    return config

def apply_config(config):
    """
    Apply the loaded configuration to the settings module.
    
    Args:
        config (dict): Configuration dictionary.
    """
    import settings

    # Apply debug settings
    settings.DEBUG = config['debug']['enabled']

    # Apply logging settings
    settings.DEFAULT_LOG_LEVEL = config['logging']['level']
    settings.LOG_FORMAT = config['logging']['format']
    settings.LOG_DATE_FORMAT = config.get('logging', {}).get('date_format', settings.LOG_DATE_FORMAT)

    # Apply game settings
    settings.SCREEN_WIDTH = config['game']['screen_width']
    settings.SCREEN_HEIGHT = config['game']['screen_height']
    settings.FPS = config['game']['fps']

    # Apply galaxy settings
    settings.NUM_STAR_SYSTEMS = config['galaxy']['num_star_systems']
    settings.NUM_BACKGROUND_STARS = config['galaxy']['num_background_stars']
    settings.NUM_NEBULAE = config['galaxy']['num_nebulae']

# Example usage in main script
# config = load_config()
# apply_config(config)
