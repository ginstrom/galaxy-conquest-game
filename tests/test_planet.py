"""Tests for the planet view module."""

import pytest
import pygame
from pygame.locals import K_ESCAPE

# Initialize pygame and font module for testing
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# Import game modules after pygame initialization
from game.views.planet import PlanetView
from game.enums import PlanetType, ResourceType, GameState
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MockGame:
    """Mock game class for testing planet view."""
    def __init__(self):
        self.info_panel_width = 300
        self.selected_planet = {
            'name': 'Test Planet',
            'type': PlanetType.TERRESTRIAL,
            'size': 10,
            'orbit_number': 1,
            'resources': [
                {'type': ResourceType.MINERALS, 'amount': 75},
                {'type': ResourceType.WATER, 'amount': 50}
            ]
        }
        self.background = MockBackground()
        self.state = GameState.PLANET
        
    def draw_info_panel(self, screen):
        """Mock info panel drawing."""
        pass

class MockBackground:
    """Mock background class for testing."""
    def draw_system_background(self, screen):
        """Mock background drawing."""
        pass

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

def test_planet_view_initialization():
    """Test PlanetView initialization."""
    game = MockGame()
    view = PlanetView(game)
    
    assert view.game == game
    assert view.available_width == SCREEN_WIDTH - game.info_panel_width
    assert view.center_x == view.available_width // 2
    assert view.center_y == SCREEN_HEIGHT // 2
    assert view.title_font is not None
    assert view.info_font is not None

def test_planet_view_draw_without_selected_planet():
    """Test drawing planet view with no selected planet."""
    game = MockGame()
    game.selected_planet = None
    view = PlanetView(game)
    
    # Create a mock screen surface
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Should not raise any errors
    view.draw(screen)

def test_planet_view_draw_with_planet():
    """Test drawing planet view with a selected planet."""
    game = MockGame()
    view = PlanetView(game)
    
    # Create a mock screen surface
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Should not raise any errors
    view.draw(screen)

def test_planet_view_handle_keydown():
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
