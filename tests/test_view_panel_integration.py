"""Tests for the integration between view classes and their InfoPanel instances."""

import pytest
import pygame
from unittest.mock import MagicMock, patch

# Initialize pygame and font module for testing
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# Import game modules after pygame initialization
from game.views.galaxy import GalaxyView
from game.views.system import SystemView
from game.views.planet import PlanetView
from game.views.infopanel import GalaxyViewInfoPanel, SystemViewInfoPanel, PlanetViewInfoPanel
from game.enums import GameState
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

def test_galaxy_view_panel_initialization():
    """Test that GalaxyView correctly initializes its InfoPanel."""
    game = MockGame()
    view = GalaxyView(game)
    
    assert view.panel is not None
    assert isinstance(view.panel, GalaxyViewInfoPanel)
    assert view.panel.game == game

def test_system_view_panel_initialization():
    """Test that SystemView correctly initializes its InfoPanel."""
    game = MockGame()
    view = SystemView(game)
    
    assert view.panel is not None
    assert isinstance(view.panel, SystemViewInfoPanel)
    assert view.panel.game == game

def test_planet_view_panel_initialization():
    """Test that PlanetView correctly initializes its InfoPanel."""
    game = MockGame()
    view = PlanetView(game)
    
    assert view.panel is not None
    assert isinstance(view.panel, PlanetViewInfoPanel)
    assert view.panel.game == game

def test_galaxy_view_uses_panel_for_drawing(mock_game, mock_screen):
    """Test that GalaxyView properly uses its panel for drawing."""
    view = GalaxyView(mock_game)
    
    # Mock the panel's draw method
    original_draw = view.panel.draw
    view.panel.draw = MagicMock()
    
    # Draw the view
    view.draw(mock_screen)
    
    # Verify that the panel's draw method was called
    view.panel.draw.assert_called_once_with(mock_screen)
    
    # Restore the original draw method
    view.panel.draw = original_draw

def test_system_view_uses_panel_for_drawing(mock_game, mock_screen):
    """Test that SystemView properly uses its panel for drawing."""
    view = SystemView(mock_game)
    
    # Ensure selected_system is not None
    mock_game.selected_system = mock_game.selected_system
    
    # Mock the panel's draw method
    original_draw = view.panel.draw
    view.panel.draw = MagicMock()
    
    # Draw the view
    view.draw(mock_screen)
    
    # Verify that the panel's draw method was called
    view.panel.draw.assert_called_once_with(mock_screen)
    
    # Restore the original draw method
    view.panel.draw = original_draw

def test_system_view_no_selected_system(mock_game, mock_screen):
    """Test SystemView behavior when no system is selected."""
    view = SystemView(mock_game)
    
    # Ensure selected_system is None
    mock_game.selected_system = None
    
    # Mock the panel's draw method
    original_draw = view.panel.draw
    view.panel.draw = MagicMock()
    
    # Draw the view
    view.draw(mock_screen)
    
    # Verify that the panel's draw method was not called
    view.panel.draw.assert_not_called()
    
    # Verify that the game state was changed to GALAXY
    assert mock_game.state == GameState.GALAXY
    
    # Restore the original draw method
    view.panel.draw = original_draw

def test_system_view_updates_hovered_planet(mock_game, mock_screen):
    """Test that SystemView correctly updates the hovered_planet attribute."""
    view = SystemView(mock_game)
    
    # Set up a selected system with planets
    mock_game.selected_system = mock_game.selected_system
    mock_game.selected_system.planets = [
        {
            'name': 'Planet 1',
            'x': 100,
            'y': 100,
            'size': 20,
            'type': MagicMock(),
            'resources': []
        },
        {
            'name': 'Planet 2',
            'x': 200,
            'y': 200,
            'size': 15,
            'type': MagicMock(),
            'resources': []
        }
    ]
    mock_game.state = GameState.SYSTEM
    
    # Mock pygame.mouse.get_pos to return a position over Planet 1
    with patch('pygame.mouse.get_pos', return_value=(100, 100)):
        # Call the update method to check for hover
        view.update()
        
        # Verify that hovered_planet is set to Planet 1
        assert mock_game.hovered_planet is not None
        assert mock_game.hovered_planet['name'] == 'Planet 1'
    
    # Mock pygame.mouse.get_pos to return a position not over any planet
    with patch('pygame.mouse.get_pos', return_value=(150, 150)):
        # Call the update method to check for hover
        view.update()
        
        # Verify that hovered_planet is None
        assert mock_game.hovered_planet is None

def test_planet_view_uses_panel_for_drawing(mock_game, mock_screen):
    """Test that PlanetView properly uses its panel for drawing."""
    view = PlanetView(mock_game)
    
    # Ensure selected_planet is not None
    mock_game.selected_planet = mock_game.selected_planet
    
    # Mock the panel's draw method
    original_draw = view.panel.draw
    view.panel.draw = MagicMock()
    
    # Draw the view
    view.draw(mock_screen)
    
    # Verify that the panel's draw method was called
    view.panel.draw.assert_called_once_with(mock_screen)
    
    # Restore the original draw method
    view.panel.draw = original_draw

def test_planet_view_no_selected_planet(mock_game, mock_screen):
    """Test PlanetView behavior when no planet is selected."""
    view = PlanetView(mock_game)
    
    # Ensure selected_planet is None
    mock_game.selected_planet = None
    
    # Mock the panel's draw method
    original_draw = view.panel.draw
    view.panel.draw = MagicMock()
    
    # Draw the view
    view.draw(mock_screen)
    
    # Verify that the panel's draw method was not called
    view.panel.draw.assert_not_called()
    
    # Restore the original draw method
    view.panel.draw = original_draw
