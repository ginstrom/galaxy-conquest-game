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

@pytest.fixture
def mock_galaxy_panel(mock_game):
    """Create a mock GalaxyViewInfoPanel."""
    panel = MagicMock(spec=GalaxyViewInfoPanel)
    panel.panel_width = 300
    panel.game = mock_game
    panel.draw = MagicMock()
    return panel

@pytest.fixture
def mock_system_panel(mock_game):
    """Create a mock SystemViewInfoPanel."""
    panel = MagicMock(spec=SystemViewInfoPanel)
    panel.panel_width = 300
    panel.game = mock_game
    panel.draw = MagicMock()
    return panel

@pytest.fixture
def mock_planet_panel(mock_game):
    """Create a mock PlanetViewInfoPanel."""
    panel = MagicMock(spec=PlanetViewInfoPanel)
    panel.panel_width = 300
    panel.game = mock_game
    panel.draw = MagicMock()
    return panel

def test_galaxy_view_panel_initialization(mock_game, mock_galaxy_panel):
    """Test that GalaxyView correctly initializes its InfoPanel."""
    with patch('game.views.galaxy.GalaxyViewInfoPanel', return_value=mock_galaxy_panel):
        view = GalaxyView(mock_game)
        
        assert view.panel is not None
        assert view.panel == mock_galaxy_panel
        assert view.panel.game == mock_game

def test_system_view_panel_initialization(mock_game, mock_system_panel):
    """Test that SystemView correctly initializes its InfoPanel."""
    with patch('game.views.system.SystemViewInfoPanel', return_value=mock_system_panel):
        view = SystemView(mock_game)
        
        assert view.panel is not None
        assert view.panel == mock_system_panel
        assert view.panel.game == mock_game

def test_planet_view_panel_initialization(mock_game, mock_planet_panel):
    """Test that PlanetView correctly initializes its InfoPanel."""
    with patch('game.views.planet.PlanetViewInfoPanel', return_value=mock_planet_panel):
        view = PlanetView(mock_game)
        
        assert view.panel is not None
        assert view.panel == mock_planet_panel
        assert view.panel.game == mock_game

def test_galaxy_view_uses_panel_for_drawing(mock_game, mock_screen, mock_galaxy_panel):
    """Test that GalaxyView properly uses its panel for drawing."""
    with patch('game.views.galaxy.GalaxyViewInfoPanel', return_value=mock_galaxy_panel):
        view = GalaxyView(mock_game)
        
        # Patch pygame.draw.line to avoid TypeError with MockSurface
        with patch('pygame.draw.line', return_value=None):
            # Draw the view
            view.draw(mock_screen)
        
        # Verify that the panel's draw method was called
        mock_galaxy_panel.draw.assert_called_once_with(mock_screen)

def test_system_view_uses_panel_for_drawing(mock_game, mock_screen, mock_system_panel):
    """Test that SystemView properly uses its panel for drawing."""
    with patch('game.views.system.SystemViewInfoPanel', return_value=mock_system_panel):
        view = SystemView(mock_game)
        
        # Ensure selected_system is not None
        mock_game.selected_system = mock_game.selected_system
        
        # Draw the view
        view.draw(mock_screen)
        
        # Verify that the panel's draw method was called
        mock_system_panel.draw.assert_called_once_with(mock_screen)

def test_system_view_no_selected_system(mock_game, mock_screen, mock_system_panel):
    """Test SystemView behavior when no system is selected."""
    with patch('game.views.system.SystemViewInfoPanel', return_value=mock_system_panel):
        view = SystemView(mock_game)
        
        # Ensure selected_system is None
        mock_game.selected_system = None
        
        # Draw the view
        view.draw(mock_screen)
        
        # Verify that the panel's draw method was not called
        mock_system_panel.draw.assert_not_called()
        
        # Verify that the game state was changed to GALAXY
        assert mock_game.state == GameState.GALAXY

def test_system_view_updates_hovered_planet(mock_game, mock_screen, mock_system_panel):
    """Test that SystemView correctly updates the hovered_planet attribute."""
    with patch('game.views.system.SystemViewInfoPanel', return_value=mock_system_panel):
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

def test_planet_view_uses_panel_for_drawing(mock_game, mock_screen, mock_planet_panel):
    """Test that PlanetView properly uses its panel for drawing."""
    with patch('game.views.planet.PlanetViewInfoPanel', return_value=mock_planet_panel):
        view = PlanetView(mock_game)
        
        # Ensure selected_planet is not None
        mock_game.selected_planet = mock_game.selected_planet
        
        # Mock the title_font and info_font to avoid errors
        view.title_font = MagicMock()
        view.title_font.render.return_value = MagicMock()
        view.title_font.render().get_rect.return_value = MagicMock()
        
        view.info_font = MagicMock()
        view.info_font.render.return_value = MagicMock()
        view.info_font.render().get_rect.return_value = MagicMock()
        
        # Patch pygame.draw.circle to avoid TypeError with MockSurface
        with patch('pygame.draw.circle', return_value=None):
            # Draw the view
            view.draw(mock_screen)
        
        # Verify that the panel's draw method was called
        mock_planet_panel.draw.assert_called_once_with(mock_screen)

def test_planet_view_no_selected_planet(mock_game, mock_screen, mock_planet_panel):
    """Test PlanetView behavior when no planet is selected."""
    with patch('game.views.planet.PlanetViewInfoPanel', return_value=mock_planet_panel):
        view = PlanetView(mock_game)
        
        # Ensure selected_planet is None
        mock_game.selected_planet = None
        
        # Draw the view
        view.draw(mock_screen)
        
        # Verify that the panel's draw method was not called
        mock_planet_panel.draw.assert_not_called()
