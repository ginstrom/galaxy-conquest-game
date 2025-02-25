"""Tests for the InfoPanel classes."""

import pytest
import pygame
from pygame.locals import K_ESCAPE

# Initialize pygame and font module for testing
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# Import game modules after pygame initialization
from game.views.infopanel import InfoPanel, GalaxyViewInfoPanel, SystemViewInfoPanel, PlanetViewInfoPanel
from game.enums import PlanetType, ResourceType, GameState
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from tests.mocks import MockGame, MockSurface

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

@pytest.fixture
def mock_game():
    """Create a mock game instance for testing."""
    return MockGame()

@pytest.fixture
def mock_screen():
    """Create a mock screen surface for testing."""
    return MockSurface((SCREEN_WIDTH, SCREEN_HEIGHT))

def test_base_infopanel_initialization():
    """Test base InfoPanel initialization."""
    game = MockGame()
    panel = InfoPanel(game)
    
    assert panel.game == game
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT
    assert panel.panel_rect.left == SCREEN_WIDTH - 300
    assert panel.panel_rect.top == 0

def test_base_infopanel_draw(mock_game, mock_screen):
    """Test base InfoPanel draw method."""
    panel = InfoPanel(mock_game)
    panel.draw(mock_screen)
    
    # The base draw method should draw the panel background and border
    # We can't easily verify the drawing operations, but we can ensure it doesn't raise errors
    assert True  # If we got here, no exceptions were raised

def test_base_infopanel_input_handlers(mock_game):
    """Test base InfoPanel input handler methods."""
    panel = InfoPanel(mock_game)
    
    # These methods should not raise errors
    panel.handle_input(None)
    panel.handle_click((0, 0))
    panel.handle_keydown(None)
    
    # If we got here, no exceptions were raised
    assert True

def test_galaxy_view_infopanel_initialization(mock_game):
    """Test GalaxyViewInfoPanel initialization."""
    panel = GalaxyViewInfoPanel(mock_game)
    
    assert panel.game == mock_game
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT

def test_galaxy_view_infopanel_draw_with_hovered_system(mock_game, mock_screen):
    """Test GalaxyViewInfoPanel draw method with a hovered system."""
    panel = GalaxyViewInfoPanel(mock_game)
    
    # Set up a hovered system
    mock_game.hovered_system = mock_game.selected_system
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True

def test_galaxy_view_infopanel_draw_without_hovered_system(mock_game, mock_screen):
    """Test GalaxyViewInfoPanel draw method without a hovered system."""
    panel = GalaxyViewInfoPanel(mock_game)
    
    # Ensure no hovered system
    mock_game.hovered_system = None
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True

def test_system_view_infopanel_initialization(mock_game):
    """Test SystemViewInfoPanel initialization."""
    panel = SystemViewInfoPanel(mock_game)
    
    assert panel.game == mock_game
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT

def test_system_view_infopanel_draw_with_selected_system(mock_game, mock_screen):
    """Test SystemViewInfoPanel draw method with a selected system."""
    panel = SystemViewInfoPanel(mock_game)
    
    # Set up a selected system
    mock_game.selected_system = mock_game.selected_system
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True

def test_system_view_infopanel_draw_with_selected_planet(mock_game, mock_screen):
    """Test SystemViewInfoPanel draw method with a selected planet."""
    panel = SystemViewInfoPanel(mock_game)
    
    # Set up a selected system and planet
    mock_game.selected_system = mock_game.selected_system
    mock_game.selected_planet = {
        'name': 'Test Planet',
        'type': PlanetType.TERRESTRIAL,
        'resources': [
            {'type': ResourceType.MINERALS, 'amount': 75},
            {'type': ResourceType.WATER, 'amount': 50}
        ]
    }
    mock_game.state = GameState.SYSTEM
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True

def test_system_view_infopanel_draw_without_selected_system(mock_game, mock_screen):
    """Test SystemViewInfoPanel draw method without a selected system."""
    panel = SystemViewInfoPanel(mock_game)
    
    # Ensure no selected system
    mock_game.selected_system = None
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True

def test_planet_view_infopanel_initialization(mock_game):
    """Test PlanetViewInfoPanel initialization."""
    panel = PlanetViewInfoPanel(mock_game)
    
    assert panel.game == mock_game
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT

def test_planet_view_infopanel_draw_with_selected_planet(mock_game, mock_screen):
    """Test PlanetViewInfoPanel draw method with a selected planet."""
    panel = PlanetViewInfoPanel(mock_game)
    
    # Set up a selected planet
    mock_game.selected_planet = {
        'name': 'Test Planet',
        'type': PlanetType.TERRESTRIAL,
        'resources': [
            {'type': ResourceType.MINERALS, 'amount': 75},
            {'type': ResourceType.WATER, 'amount': 50}
        ]
    }
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True

def test_planet_view_infopanel_draw_without_selected_planet(mock_game, mock_screen):
    """Test PlanetViewInfoPanel draw method without a selected planet."""
    panel = PlanetViewInfoPanel(mock_game)
    
    # Ensure no selected planet
    mock_game.selected_planet = None
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # If we got here, no exceptions were raised
    assert True
