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
from game.planet import Planet
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


# Tests for the Planet class
def test_planet_initialization():
    """Test Planet class initialization."""
    resources_dict = {
        ResourceType.MINERALS: 75,
        ResourceType.WATER: 50
    }
    
    planet = Planet(
        name="Test Planet",
        planet_type=PlanetType.TERRESTRIAL,
        size=10,
        orbit_number=1,
        angle=0.5,
        orbit_speed=0.3,
        resources=resources_dict
    )
    
    assert planet.name == "Test Planet"
    assert planet.type == PlanetType.TERRESTRIAL
    assert planet.size == 10
    assert planet.orbit_number == 1
    assert planet.angle == 0.5
    assert planet.orbit_speed == 0.3
    assert len(planet.resources) == 2
    assert planet.resources[ResourceType.MINERALS] == 75
    assert planet.resources[ResourceType.WATER] == 50
    assert planet.x is None
    assert planet.y is None

def test_planet_from_dict():
    """Test creating a Planet from a dictionary."""
    planet_dict = {
        'name': 'Dict Planet',
        'type': PlanetType.GAS_GIANT,
        'size': 15,
        'orbit_number': 2,
        'angle': 1.0,
        'orbit_speed': 0.2,
        'resources': [
            {'type': ResourceType.GASES, 'amount': 90},
            {'type': ResourceType.ENERGY, 'amount': 60}
        ],
        'x': 100,
        'y': 200
    }
    
    planet = Planet.from_dict(planet_dict)
    
    assert planet.name == 'Dict Planet'
    assert planet.type == PlanetType.GAS_GIANT
    assert planet.size == 15
    assert planet.orbit_number == 2
    assert planet.angle == 1.0
    assert planet.orbit_speed == 0.2
    # Resources are now stored as a dictionary with resource types as keys
    assert len(planet.resources) == 2
    assert planet.resources[ResourceType.GASES] == 90
    assert planet.resources[ResourceType.ENERGY] == 60
    assert planet.x == 100
    assert planet.y == 200

def test_planet_to_dict():
    """Test converting a Planet to a dictionary."""
    resources_dict = {
        ResourceType.MINERALS: 75,
        ResourceType.WATER: 50
    }
    
    planet = Planet(
        name="Test Planet",
        planet_type=PlanetType.TERRESTRIAL,
        size=10,
        orbit_number=1,
        angle=0.5,
        orbit_speed=0.3,
        resources=resources_dict
    )
    planet.x = 150
    planet.y = 250
    
    planet_dict = planet.to_dict()
    
    assert planet_dict['name'] == "Test Planet"
    assert planet_dict['type'] == PlanetType.TERRESTRIAL
    assert planet_dict['size'] == 10
    assert planet_dict['orbit_number'] == 1
    assert planet_dict['angle'] == 0.5
    assert planet_dict['orbit_speed'] == 0.3
    assert planet_dict['resources'] == resources_dict
    assert planet_dict['x'] == 150
    assert planet_dict['y'] == 250

def test_planet_generate():
    """Test generating a random planet."""
    planet = Planet.generate("Test System", 3)
    
    assert planet.name == "Test System 3"
    assert isinstance(planet.type, PlanetType)
    assert planet.size > 0
    assert planet.orbit_number == 3
    assert planet.angle is not None
    assert planet.orbit_speed is not None
    assert isinstance(planet.resources, dict)
    assert planet.x is None
    assert planet.y is None

def test_planet_dict_access():
    """Test dictionary-like access to Planet attributes."""
    resources_dict = {
        ResourceType.MINERALS: 75,
        ResourceType.WATER: 50
    }
    
    planet = Planet(
        name="Test Planet",
        planet_type=PlanetType.TERRESTRIAL,
        size=10,
        orbit_number=1,
        angle=0.5,
        orbit_speed=0.3,
        resources=resources_dict
    )
    planet.x = 150
    planet.y = 250
    
    assert planet['name'] == "Test Planet"
    assert planet['type'] == PlanetType.TERRESTRIAL
    assert planet['size'] == 10
    assert planet['orbit_number'] == 1
    assert planet['angle'] == 0.5
    assert planet['orbit_speed'] == 0.3
    assert planet['resources'] == resources_dict
    assert planet['x'] == 150
    assert planet['y'] == 250
    
    # Test accessing a non-existent key
    with pytest.raises(KeyError):
        _ = planet['non_existent_key']
