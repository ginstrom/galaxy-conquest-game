"""Tests for the main Game class."""
import pytest
import pygame
from galaxy_conquest import Game
from game.enums import GameState

@pytest.fixture
def game(mock_pygame):
    """Create a game instance for testing."""
    # Patch pygame modules
    import pygame
    import sys
    
    # Create a mock pygame module
    mock_module = type(sys)(pygame.__name__)
    mock_module.__dict__.update({
        'init': mock_pygame.init,
        'display': mock_pygame.display,
        'font': mock_pygame.font,
        'mixer': mock_pygame.mixer,
        'Surface': mock_pygame.Surface,
        'draw': mock_pygame.draw,
        'image': mock_pygame.image,
        'error': mock_pygame.error,
        'SRCALPHA': mock_pygame.SRCALPHA,
        'Rect': pygame.Rect  # Add Rect class from pygame
    })
    
    # Save original module
    original_pygame = sys.modules[pygame.__name__]
    
    # Replace with mock
    sys.modules[pygame.__name__] = mock_module
    
    try:
        game_instance = Game()
        return game_instance
    finally:
        # Restore original module
        sys.modules[pygame.__name__] = original_pygame

def test_game_initialization(game):
    """Test that the game is properly initialized."""
    assert game.state == GameState.STARTUP_MENU
    assert game.selected_system is None
    assert game.selected_planet is None
    assert game.hovered_system is None
    assert isinstance(game.star_systems, list)
    assert pygame.display.get_surface() is not None

def test_menu_creation(game):
    """Test that menus are properly created."""
    # Test startup menu items
    startup_items = game.startup_view.menu.items
    assert any(item.text == "New Game" for item in startup_items)
    assert any(item.text == "Load Game" for item in startup_items)
    assert any(item.text == "Exit" for item in startup_items)

def test_resource_loading(game):
    """Test that game resources are properly loaded."""
    assert 'desert' in game.planet_images
    assert 'oceanic' in game.planet_images
    assert game.title_font is not None
    assert game.info_font is not None
    assert game.detail_font is not None
