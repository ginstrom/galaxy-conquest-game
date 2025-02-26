"""
Extended Test Suite for game.py

This module adds additional tests for the Game class in game/game.py,
improving the overall test coverage.
"""

import pytest
import pygame
from unittest.mock import patch, MagicMock
from game.game import Game
from game.enums import GameState
from tests.mocks import MockSurface

# Dummy implementations for save/load functions used in testing.
def dummy_save_game_state(star_systems, selected_system):
    dummy_save_game_state.called = True
    dummy_save_game_state.star_systems = star_systems
    dummy_save_game_state.selected_system = selected_system

dummy_save_game_state.called = False

def dummy_load_game_state():
    from game.enums import StarType
    return {
        'star_systems': [
            {
                'x': 100,
                'y': 200,
                'name': 'TestSystem1',
                'star_type': StarType.MAIN_SEQUENCE,
                'size': 10,
                'color': [255, 255, 255],
                'planets': []
            }
        ]
    }

@pytest.fixture
def game_with_mocks(mock_pygame, resource_manager):
    """Create a Game instance with mocked dependencies for testing."""
    with patch('game.game.ResourceManagerFactory.create', return_value=resource_manager):
        game = Game()
        # Mock the views to avoid initialization issues
        game.startup_view = MagicMock()
        game.galaxy_view = MagicMock()
        game.system_view = MagicMock()
        game.planet_view = MagicMock()
        return game

def test_new_game(game_with_mocks):
    """Test the new_game method."""
    game = game_with_mocks
    # Override generate_star_systems to simulate creation
    game.generate_star_systems = MagicMock()
    
    result = game.new_game()
    
    assert result is True
    assert game.state == GameState.GALAXY
    assert game.current_view == game.galaxy_view
    assert game.generate_star_systems.called

def test_go_to_galaxy_view(game_with_mocks):
    """Test the go_to_galaxy_view method."""
    game = game_with_mocks
    game.state = GameState.SYSTEM
    
    result = game.go_to_galaxy_view()
    
    assert result is True
    assert game.state == GameState.GALAXY
    assert game.current_view == game.galaxy_view

def test_save_game_from_galaxy(game_with_mocks, monkeypatch):
    """Test saving the game from galaxy view."""
    game = game_with_mocks
    monkeypatch.setattr('game.game.save_game_state', dummy_save_game_state)
    dummy_save_game_state.called = False
    
    # Test non-menu call
    game.state = GameState.GALAXY
    game.selected_system = None
    
    result = game.save_game()
    
    assert dummy_save_game_state.called is True
    assert result is False  # Non-menu call returns False

def test_save_game_from_menu_with_system(game_with_mocks, monkeypatch):
    """Test saving the game from menu with a selected system."""
    game = game_with_mocks
    monkeypatch.setattr('game.game.save_game_state', dummy_save_game_state)
    dummy_save_game_state.called = False
    
    # Test menu call with selected system
    game.state = GameState.GALAXY_MENU
    game.selected_system = MagicMock()
    
    result = game.save_game()
    
    assert dummy_save_game_state.called is True
    assert result is True  # Menu call returns True
    assert game.state == GameState.SYSTEM
    assert game.current_view == game.system_view

def test_save_game_from_menu_without_system(game_with_mocks, monkeypatch):
    """Test saving the game from menu without a selected system."""
    game = game_with_mocks
    monkeypatch.setattr('game.game.save_game_state', dummy_save_game_state)
    dummy_save_game_state.called = False
    
    # Test menu call without selected system
    game.state = GameState.GALAXY_MENU
    game.selected_system = None
    
    result = game.save_game()
    
    assert dummy_save_game_state.called is True
    assert result is True  # Menu call returns True
    assert game.state == GameState.GALAXY
    assert game.current_view == game.galaxy_view

def test_load_game_success(game_with_mocks, monkeypatch):
    """Test successfully loading a game."""
    game = game_with_mocks
    monkeypatch.setattr('game.game.load_game_state', dummy_load_game_state)
    
    result = game.load_game()
    
    assert result is True
    assert len(game.star_systems) == 1
    assert game.star_systems[0].name == 'TestSystem1'
    assert game.state == GameState.GALAXY
    assert game.current_view == game.galaxy_view

def test_load_game_failure(game_with_mocks, monkeypatch):
    """Test handling a failed game load."""
    game = game_with_mocks
    
    def failing_load_game_state():
        raise FileNotFoundError("No save file found")
    
    monkeypatch.setattr('game.game.load_game_state', failing_load_game_state)
    
    result = game.load_game()
    
    assert result is False

def test_continue_game(game_with_mocks):
    """Test the continue_game method."""
    game = game_with_mocks
    game.load_game = MagicMock(return_value=True)
    
    result = game.continue_game()
    
    assert result is True
    assert game.load_game.called

def test_return_to_game_with_system(game_with_mocks):
    """Test returning to game with a selected system."""
    game = game_with_mocks
    game.selected_system = MagicMock()
    
    result = game.return_to_game()
    
    assert result is True
    assert game.state == GameState.SYSTEM
    assert game.current_view == game.system_view

def test_return_to_game_without_system(game_with_mocks):
    """Test returning to game without a selected system."""
    game = game_with_mocks
    game.selected_system = None
    
    result = game.return_to_game()
    
    assert result is True
    assert game.state == GameState.GALAXY
    assert game.current_view == game.galaxy_view

def test_quit_to_main_menu(game_with_mocks):
    """Test quitting to the main menu."""
    game = game_with_mocks
    game.selected_system = MagicMock()
    game.selected_planet = MagicMock()
    
    result = game.quit_to_main_menu()
    
    assert result is True
    assert game.state == GameState.STARTUP_MENU
    assert game.current_view == game.startup_view
    assert game.selected_system is None
    assert game.selected_planet is None

def test_quit_game(game_with_mocks):
    """Test quitting the game."""
    game = game_with_mocks
    
    result = game.quit_game()
    
    assert result is False

def test_generate_star_systems(game_with_mocks, monkeypatch):
    """Test generating star systems."""
    game = game_with_mocks
    
    # Mock random.randint to return predictable values
    monkeypatch.setattr('random.randint', lambda min_val, max_val: (min_val + max_val) // 2)
    
    # Mock StarSystem to avoid collisions
    class MockStarSystem:
        def __init__(self, x, y, game_instance, **kwargs):
            self.x = x
            self.y = y
            self.game = game_instance
            self.name = kwargs.get('name', 'MockSystem')
            self.collides_with = MagicMock(return_value=False)
    
    monkeypatch.setattr('game.game.StarSystem', MockStarSystem)
    
    # Mock galaxy_rect for positioning
    game.galaxy_view.galaxy_rect = pygame.Rect(0, 0, 800, 600)
    
    # Test the method
    game.generate_star_systems()
    
    # Check that star systems were created
    assert len(game.star_systems) > 0

def test_draw_save_notification(game_with_mocks, monkeypatch):
    """Test drawing the save notification."""
    game = game_with_mocks
    
    # Set up the notification time to be recent
    current_time = 1000
    monkeypatch.setattr('pygame.time.get_ticks', lambda: current_time)
    game.save_notification_time = current_time - 500  # 500ms ago
    game.save_notification_duration = 2000  # 2 seconds
    
    # Create a mock surface to draw on
    screen = MockSurface((800, 600))
    
    # Mock the font rendering
    mock_text_surface = MockSurface((100, 30))
    game.info_font.render = MagicMock(return_value=mock_text_surface)
    
    # Test the method
    game.draw_save_notification(screen)
    
    # Verify that the font was used to render text
    assert game.info_font.render.called
    
    # Test when notification should not be shown
    game.save_notification_time = current_time - 3000  # 3 seconds ago (expired)
    game.info_font.render.reset_mock()
    
    game.draw_save_notification(screen)
    
    # Verify that the font was not used to render text
    assert not game.info_font.render.called

def test_cleanup(game_with_mocks):
    """Test the cleanup method."""
    game = game_with_mocks
    game.resource_manager.cleanup = MagicMock()
    pygame_quit = MagicMock()
    
    with patch('pygame.quit', pygame_quit):
        game.cleanup()
    
    assert game.resource_manager.cleanup.called
    assert pygame_quit.called
