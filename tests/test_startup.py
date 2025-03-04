"""
Tests for the startup view module.
"""

import pytest
import pygame
from unittest.mock import Mock, patch

from game.views.startup import StartupView
from game.enums import GameState


@pytest.fixture
def mock_game():
    """Create a mock game instance with required attributes."""
    game = Mock()
    game.state = GameState.STARTUP_MENU
    return game


@pytest.fixture
def startup_view(mock_game):
    """Create a StartupView instance with a mock game."""
    return StartupView(mock_game)


def test_startup_view_initialization(startup_view):
    """Test that StartupView initializes correctly."""
    assert startup_view.menu is not None
    assert len(startup_view.menu.items) == 3
    assert startup_view.menu.items[0].text == "New Game"
    assert startup_view.menu.items[1].text == "Load Game"
    assert startup_view.menu.items[2].text == "Exit"


def test_start_new_game(startup_view, mock_game):
    """Test starting a new game."""
    result = startup_view.start_new_game()
    
    assert result is True
    assert mock_game.new_game.called


@patch('game.views.startup.save_exists')
def test_load_game_disabled_when_no_save(mock_save_exists, mock_game):
    """Test that load game option is disabled when no save file exists."""
    mock_save_exists.return_value = False
    view = StartupView(mock_game)
    
    assert view.menu.items[1].enabled is False


def test_load_game_success(startup_view, mock_game):
    """Test loading a game successfully."""
    mock_game.load_game.return_value = True
    result = startup_view.load_game()
    
    assert result is True


def test_load_game_failure(startup_view, mock_game):
    """Test handling a failed game load."""
    mock_game.load_game.return_value = False
    result = startup_view.load_game()
    
    assert result is True  # Keep game running even if load fails


def test_exit_game(startup_view):
    """Test exiting the game."""
    result = startup_view.exit_game()
    assert result is False


@pytest.mark.parametrize("key,expected_handled", [
    (pygame.K_UP, True),
    (pygame.K_DOWN, True),
    (pygame.K_RETURN, True),
    (pygame.K_ESCAPE, False),
])
def test_handle_keydown(startup_view, key, expected_handled):
    """Test keyboard input handling for various key events."""
    event = Mock()
    event.type = pygame.KEYDOWN
    event.key = key
    
    if expected_handled:
        startup_view.menu.handle_input = Mock(return_value=True)
        result = startup_view.handle_keydown(event)
        assert result is True
        assert startup_view.menu.handle_input.called
    else:
        result = startup_view.handle_keydown(event)
        assert result is None


def test_handle_input_keydown(startup_view):
    """Test that handle_input correctly delegates keyboard events."""
    event = Mock()
    event.type = pygame.KEYDOWN
    event.key = pygame.K_RETURN
    
    startup_view.handle_keydown = Mock(return_value=True)
    result = startup_view.handle_input(event)
    
    assert result is True
    startup_view.handle_keydown.assert_called_once_with(event)


def test_handle_input_mousedown(startup_view):
    """Test that handle_input correctly delegates mouse events."""
    event = Mock()
    event.type = pygame.MOUSEBUTTONDOWN
    event.pos = (100, 100)
    
    startup_view.handle_click = Mock(return_value=True)
    result = startup_view.handle_input(event)
    
    assert result is True
    startup_view.handle_click.assert_called_once_with(event.pos)


def test_handle_click_creates_correct_event(startup_view):
    """Test that handle_click creates the correct event with button attribute."""
    pos = (100, 100)
    startup_view.menu.handle_input = Mock(return_value=True)
    
    result = startup_view.handle_click(pos)
    
    assert result is True
    # Verify the event passed to menu.handle_input
    call_args = startup_view.menu.handle_input.call_args[0][0]
    assert call_args.type == pygame.MOUSEBUTTONDOWN
    assert call_args.pos == pos
    assert call_args.button == 1


def test_draw(startup_view):
    """Test drawing the startup view."""
    screen = Mock()
    startup_view.background.draw_galaxy_background = Mock()
    
    startup_view.draw(screen)
    
    startup_view.background.draw_galaxy_background.assert_called_once_with(screen)
