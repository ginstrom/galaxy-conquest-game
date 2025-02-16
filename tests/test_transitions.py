"""
Tests for the view transition system.
"""

import pytest
import pygame
from unittest.mock import Mock, patch

from game.transitions import ViewTransition, ViewStateManager


@pytest.fixture
def view_transition():
    """Create a ViewTransition instance."""
    return ViewTransition(duration_ms=500)


@pytest.fixture
def view_state_manager():
    """Create a ViewStateManager instance."""
    return ViewStateManager()


def test_view_transition_initialization(view_transition):
    """Test that ViewTransition initializes correctly."""
    assert view_transition.duration == 500
    assert view_transition.start_time == 0
    assert view_transition.is_active is False
    assert view_transition.from_view is None
    assert view_transition.to_view is None


@patch('pygame.time.get_ticks')
def test_view_transition_start(mock_get_ticks, view_transition):
    """Test starting a transition."""
    mock_get_ticks.return_value = 1000
    view_transition.start("menu", "game")  # Fixed string concatenation bug

    assert view_transition.is_active is True
    assert view_transition.from_view == "menu"
    assert view_transition.to_view == "game"
    assert view_transition.start_time == 1000


@patch('pygame.time.get_ticks')
def test_view_transition_draw_inactive(mock_get_ticks, view_transition):
    """Test drawing when transition is inactive."""
    mock_screen = Mock()
    
    result = view_transition.draw(mock_screen)
    
    assert result is False
    assert not mock_screen.blit.called


@patch('pygame.time.get_ticks')
def test_view_transition_draw_active(mock_get_ticks, view_transition):
    """Test drawing an active transition."""
    mock_screen = Mock()
    mock_screen.get_size.return_value = (800, 600)
    
    # Start transition
    mock_get_ticks.return_value = 1000
    view_transition.start("menu", "game")
    
    # Draw halfway through transition
    mock_get_ticks.return_value = 1250  # 500ms / 2
    result = view_transition.draw(mock_screen)
    
    assert result is True
    assert mock_screen.blit.called


@patch('pygame.time.get_ticks')
def test_view_transition_completion(mock_get_ticks, view_transition):
    """Test transition completion."""
    mock_screen = Mock()
    mock_screen.get_size.return_value = (800, 600)
    
    # Start transition
    mock_get_ticks.return_value = 1000
    view_transition.start("menu", "game")
    
    # Draw after duration
    mock_get_ticks.return_value = 1600  # > 500ms
    result = view_transition.draw(mock_screen)
    
    assert result is False
    assert view_transition.is_active is False


def test_view_state_manager_initialization(view_state_manager):
    """Test that ViewStateManager initializes correctly."""
    assert view_state_manager.view_states == {}
    assert view_state_manager.current_view is None


def test_view_state_manager_store_state(view_state_manager):
    """Test storing view state."""
    state_data = {"position": (100, 200), "score": 500}
    view_state_manager.store_state("game_view", state_data)
    
    assert "game_view" in view_state_manager.view_states
    assert view_state_manager.view_states["game_view"] == state_data


def test_view_state_manager_get_state(view_state_manager):
    """Test retrieving view state."""
    state_data = {"level": 1, "health": 100}
    view_state_manager.store_state("level_view", state_data)
    
    retrieved_state = view_state_manager.get_state("level_view")
    assert retrieved_state == state_data


def test_view_state_manager_get_nonexistent_state(view_state_manager):
    """Test retrieving state for nonexistent view."""
    assert view_state_manager.get_state("nonexistent_view") is None


def test_view_state_manager_clear_state(view_state_manager):
    """Test clearing view state."""
    state_data = {"inventory": ["sword", "shield"]}
    view_state_manager.store_state("inventory_view", state_data)
    
    view_state_manager.clear_state("inventory_view")
    assert "inventory_view" not in view_state_manager.view_states


def test_view_state_manager_clear_nonexistent_state(view_state_manager):
    """Test clearing nonexistent view state."""
    # Should not raise an error
    view_state_manager.clear_state("nonexistent_view")


def test_view_state_manager_multiple_states(view_state_manager):
    """Test managing multiple view states."""
    states = {
        "menu": {"selected": 2},
        "game": {"score": 1000},
        "inventory": {"items": ["potion"]}
    }
    
    for view, state in states.items():
        view_state_manager.store_state(view, state)
    
    for view, state in states.items():
        assert view_state_manager.get_state(view) == state


def test_view_state_manager_update_existing_state(view_state_manager):
    """Test updating existing view state."""
    initial_state = {"score": 100}
    updated_state = {"score": 200}
    
    view_state_manager.store_state("game", initial_state)
    view_state_manager.store_state("game", updated_state)
    
    assert view_state_manager.get_state("game") == updated_state
