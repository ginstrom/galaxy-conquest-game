"""Tests for the planet view module."""

import pytest
import pygame
from pygame.locals import K_ESCAPE
from unittest.mock import MagicMock, patch

# Initialize pygame and font module for testing
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# Import game modules after pygame initialization
from game.views.planet import PlanetView
from game.enums import PlanetType, ResourceType, GameState
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from tests.mocks import MockGame, MockInfoPanel

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

@pytest.fixture
def mock_planet_view_info_panel():
    """Mock the PlanetViewInfoPanel class."""
    with patch('game.views.planet.PlanetViewInfoPanel') as mock_panel_class:
        # Create a MagicMock instance instead of using MockInfoPanel
        mock_panel = MagicMock()
        mock_panel.panel_width = 300
        mock_panel.panel_rect = pygame.Rect(0, 0, 300, 600)
        mock_panel.draw = MagicMock()
        
        # Configure the mock class to return our mock panel
        mock_panel_class.return_value = mock_panel
        yield mock_panel_class

def test_planet_view_initialization(mock_planet_view_info_panel):
    """Test PlanetView initialization."""
    game = MockGame()
    view = PlanetView(game)
    
    assert view.game == game
    assert view.available_width == SCREEN_WIDTH - view.panel.panel_width
    assert view.center_x == view.available_width // 2
    assert view.center_y == SCREEN_HEIGHT // 2
    assert view.title_font is not None
    assert view.info_font is not None

def test_planet_view_draw_without_selected_planet(mock_planet_view_info_panel):
    """Test drawing planet view with no selected planet."""
    game = MockGame()
    game.selected_planet = None
    view = PlanetView(game)
    
    # Create a mock screen surface
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Should not raise any errors
    view.draw(screen)

def test_planet_view_draw_with_planet(mock_planet_view_info_panel):
    """Test drawing planet view with a selected planet."""
    game = MockGame()
    view = PlanetView(game)
    
    # Create a mock screen surface
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Mock pygame.draw.circle to avoid errors with Surface objects
    with patch('pygame.draw.circle'):
        # Should not raise any errors
        view.draw(screen)

def test_planet_view_handle_keydown(mock_planet_view_info_panel):
    """Test planet view key press handling."""
    game = MockGame()
    view = PlanetView(game)
    
    # Create a mock key event
    event = pygame.event.Event(pygame.KEYDOWN, {'key': K_ESCAPE})
    
    # Handle the key press
    view.handle_keydown(event)
    
    # Verify state changes
    assert game.state == GameState.SYSTEM
    assert game.selected_planet is None
