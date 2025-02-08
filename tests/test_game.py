"""Tests for the main Game class."""
import pytest
import pygame
from galaxy_conquest import Game
from game.enums import GameState

@pytest.fixture
def game():
    """Create a game instance for testing."""
    return Game()

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
    assert hasattr(game, 'startup_menu')
    assert hasattr(game, 'galaxy_menu')
    assert hasattr(game, 'system_menu')
    
    # Test startup menu items
    startup_items = game.startup_menu.items
    assert any(item.text == "New Game" for item in startup_items)
    assert any(item.text == "Continue" for item in startup_items)
    assert any(item.text == "Quit" for item in startup_items)

def test_resource_loading(game):
    """Test that game resources are properly loaded."""
    assert 'desert' in game.planet_images
    assert 'oceanic' in game.planet_images
    assert game.title_font is not None
    assert game.info_font is not None
    assert game.detail_font is not None
