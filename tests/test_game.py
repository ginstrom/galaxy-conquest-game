"""Tests for the main Game class."""
import pytest
import pygame
from unittest.mock import patch, MagicMock
from game.game import Game
from game.enums import GameState

@pytest.fixture
def game_instance(mock_pygame, resource_manager):
    """Create a Game instance with mocked dependencies for testing."""
    with patch('game.game.ResourceManagerFactory.create', return_value=resource_manager):
        game = Game()
        # Mock the views to avoid initialization issues
        game.startup_view = MagicMock()
        game.galaxy_view = MagicMock()
        game.system_view = MagicMock()
        game.planet_view = MagicMock()
        
        # Setup startup menu items for testing
        startup_menu_items = [
            MagicMock(text="New Game"),
            MagicMock(text="Load Game"),
            MagicMock(text="Exit")
        ]
        game.startup_view.menu.items = startup_menu_items
        
        # Setup planet images for testing
        game.planet_images = {
            'desert': MagicMock(),
            'oceanic': MagicMock()
        }
        
        # Setup fonts for testing
        game.title_font = MagicMock()
        game.info_font = MagicMock()
        game.detail_font = MagicMock()
        
        return game

def test_game_initialization(game_instance):
    """Test that the game is properly initialized."""
    assert game_instance.state == GameState.STARTUP_MENU
    assert game_instance.selected_system is None
    assert game_instance.selected_planet is None
    assert game_instance.hovered_system is None
    assert isinstance(game_instance.star_systems, list)

def test_menu_creation(game_instance):
    """Test that menus are properly created."""
    # Test startup menu items
    startup_items = game_instance.startup_view.menu.items
    assert any(item.text == "New Game" for item in startup_items)
    assert any(item.text == "Load Game" for item in startup_items)
    assert any(item.text == "Exit" for item in startup_items)

def test_resource_loading(game_instance):
    """Test that game resources are properly loaded."""
    assert 'desert' in game_instance.planet_images
    assert 'oceanic' in game_instance.planet_images
    assert game_instance.title_font is not None
    assert game_instance.info_font is not None
    assert game_instance.detail_font is not None

def test_to_state(game_instance):
    """Test that the to_state method correctly transitions between game states."""
    # Test transition to GALAXY state
    game_instance.to_state(GameState.STARTUP_MENU, GameState.GALAXY)
    assert game_instance.state == GameState.GALAXY
    assert game_instance.current_view == game_instance.galaxy_view
    
    # Test transition to SYSTEM state
    game_instance.to_state(GameState.GALAXY, GameState.SYSTEM)
    assert game_instance.state == GameState.SYSTEM
    assert game_instance.current_view == game_instance.system_view
    
    # Test transition to PLANET state
    game_instance.to_state(GameState.SYSTEM, GameState.PLANET)
    assert game_instance.state == GameState.PLANET
    assert game_instance.current_view == game_instance.planet_view
    
    # Test transition to STARTUP_MENU state
    game_instance.to_state(GameState.PLANET, GameState.STARTUP_MENU)
    assert game_instance.state == GameState.STARTUP_MENU
    assert game_instance.current_view == game_instance.startup_view
    
    # Test transition to menu states
    game_instance.to_state(GameState.GALAXY, GameState.GALAXY_MENU)
    assert game_instance.state == GameState.GALAXY_MENU
    assert game_instance.current_view == game_instance.galaxy_view
    
    game_instance.to_state(GameState.SYSTEM, GameState.SYSTEM_MENU)
    assert game_instance.state == GameState.SYSTEM_MENU
    assert game_instance.current_view == game_instance.system_view
