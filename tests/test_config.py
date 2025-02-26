"""Tests for the configuration module."""
import os
import sys
import pytest
from unittest.mock import mock_open, patch, MagicMock
import argparse
from game.config import load_config, apply_config, parse_arguments

# Sample configuration for testing
SAMPLE_CONFIG = """
[debug]
enabled = true

[logging]
level = "INFO"
format = "%(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

[game]
screen_width = 1024
screen_height = 768
fps = 60

[galaxy]
num_star_systems = 15
num_background_stars = 300
num_nebulae = 5
"""

@pytest.fixture
def mock_settings():
    """Mock the settings module for testing."""
    # Create a mock settings module
    mock_settings = MagicMock()
    mock_settings.DEBUG = False
    mock_settings.DEFAULT_LOG_LEVEL = "DEBUG"
    mock_settings.LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    mock_settings.LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    mock_settings.SCREEN_WIDTH = 800
    mock_settings.SCREEN_HEIGHT = 600
    mock_settings.FPS = 30
    mock_settings.NUM_STAR_SYSTEMS = 10
    mock_settings.NUM_BACKGROUND_STARS = 200
    mock_settings.NUM_NEBULAE = 3
    
    # Store original settings module if it exists
    original_settings = sys.modules.get('settings', None)
    
    # Replace with our mock
    sys.modules['settings'] = mock_settings
    
    yield mock_settings
    
    # Restore original settings module
    if original_settings:
        sys.modules['settings'] = original_settings
    else:
        del sys.modules['settings']

@pytest.fixture(autouse=True)
def mock_gettext():
    """Mock gettext to avoid bytes issues with mock_open."""
    with patch('gettext.find'), \
         patch('gettext.translation'), \
         patch('gettext.gettext', side_effect=lambda x: x):
        yield

def test_load_config_defaults(mock_settings):
    """Test loading default configuration when no file exists."""
    with patch('os.path.exists', return_value=False):
        config = load_config('nonexistent.toml', args=[])
        
        assert config['debug']['enabled'] == mock_settings.DEBUG
        assert config['logging']['level'] == mock_settings.DEFAULT_LOG_LEVEL
        assert config['game']['screen_width'] == mock_settings.SCREEN_WIDTH
        assert config['galaxy']['num_star_systems'] == mock_settings.NUM_STAR_SYSTEMS

def test_load_config_from_toml(mock_settings):
    """Test loading configuration from TOML file."""
    mock_file = mock_open(read_data=SAMPLE_CONFIG)
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_file):
        config = load_config('config/prefs.toml', args=[])
        
        assert config['debug']['enabled'] is True
        assert config['logging']['level'] == "INFO"
        assert config['game']['screen_width'] == 1024
        assert config['galaxy']['num_star_systems'] == 15

def test_load_config_with_cli_override(mock_settings):
    """Test command-line arguments overriding configuration."""
    test_args = ['--debug', 'True', '--screen-width', '1280', '--num-star-systems', '20']
    with patch('os.path.exists', return_value=False):
        config = load_config('config/prefs.toml', args=test_args)
        
        assert config['debug']['enabled'] is True
        assert config['game']['screen_width'] == 1280
        assert config['galaxy']['num_star_systems'] == 20

def test_apply_config(mock_settings):
    """Test applying configuration to settings module."""
    config = {
        'debug': {'enabled': True},
        'logging': {
            'level': "INFO",
            'format': "%(levelname)s - %(message)s",
            'date_format': "%Y-%m-%d %H:%M:%S"
        },
        'game': {
            'screen_width': 1024,
            'screen_height': 768,
            'fps': 60
        },
        'galaxy': {
            'num_star_systems': 15,
            'num_background_stars': 300,
            'num_nebulae': 5
        }
    }
    
    apply_config(config)
    
    assert mock_settings.DEBUG is True
    assert mock_settings.DEFAULT_LOG_LEVEL == "INFO"
    assert mock_settings.SCREEN_WIDTH == 1024
    assert mock_settings.NUM_STAR_SYSTEMS == 15

def test_parse_arguments():
    """Test parsing command-line arguments."""
    test_args = [
        '--log-level', 'INFO',
        '--debug', 'True',
        '--screen-width', '1280',
        '--screen-height', '720',
        '--fps', '60',
        '--num-star-systems', '20',
        '--num-background-stars', '400',
        '--num-nebulae', '6'
    ]
    
    with patch('sys.argv', ['script.py'] + test_args):
        args = parse_arguments(None)  # None since we're mocking sys.argv
        
        assert args.log_level == 'INFO'
        assert args.debug is True
        assert args.screen_width == 1280
        assert args.screen_height == 720
        assert args.fps == 60
        assert args.num_star_systems == 20
        assert args.num_background_stars == 400
        assert args.num_nebulae == 6

def test_load_config_invalid_toml(mock_settings):
    """Test handling of invalid TOML configuration."""
    invalid_config = "invalid = toml [ content"
    mock_file = mock_open(read_data=invalid_config)
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_file), \
         patch('builtins.print') as mock_print:
        config = load_config('config/prefs.toml', args=[])
        
        # Should fall back to default values
        assert config['debug']['enabled'] == mock_settings.DEBUG
        assert config['logging']['level'] == mock_settings.DEFAULT_LOG_LEVEL
        assert mock_print.called  # Warning should be printed

def test_load_config_partial_toml(mock_settings):
    """Test loading partial TOML configuration."""
    partial_config = """
    [game]
    screen_width = 1024
    screen_height = 768
    """
    mock_file = mock_open(read_data=partial_config)
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_file):
        config = load_config('config/prefs.toml', args=[])
        
        # Specified values should be loaded
        assert config['game']['screen_width'] == 1024
        assert config['game']['screen_height'] == 768
        
        # Unspecified values should use defaults
        assert config['debug']['enabled'] == mock_settings.DEBUG
        assert config['logging']['level'] == mock_settings.DEFAULT_LOG_LEVEL
