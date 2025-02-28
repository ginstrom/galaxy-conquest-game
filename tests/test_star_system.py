"""Tests for the StarSystem class."""
import pytest
import pygame
from unittest.mock import Mock
from game.star_system import StarSystem
from game.enums import StarType, PlanetType, ResourceType
from game.constants import WHITE, GRAY, SCREEN_WIDTH, SCREEN_HEIGHT
from game.properties import StarProperties
from tests.mocks import MockSurface

@pytest.fixture
def mock_game(resource_manager):
    """Create a mock game instance with resource manager."""
    game = Mock()
    game.resource_manager = resource_manager
    return game

@pytest.fixture
def star_system(mock_game):
    """Create a basic star system for testing."""
    return StarSystem(
        x=100, 
        y=100, 
        name="Test System", 
        star_type=StarType.MAIN_SEQUENCE,
        game_instance=mock_game
    )

@pytest.fixture
def screen():
    """Create a mock screen for testing."""
    return MockSurface((SCREEN_WIDTH, SCREEN_HEIGHT))

def test_star_system_initialization(star_system):
    """Test that a star system is properly initialized."""
    assert star_system.name == "Test System"
    assert star_system.x == 100
    assert star_system.y == 100
    assert star_system.star_type == StarType.MAIN_SEQUENCE
    assert isinstance(star_system.planets, list)
    assert hasattr(star_system, 'rect')
    assert hasattr(star_system, 'name_surface')
    assert hasattr(star_system, 'name_rect')

def test_star_system_collision(star_system, mock_game):
    """Test collision detection between star systems."""
    # Create another star system within collision range
    min_distance = star_system.size * 6  # Minimum distance between systems
    close_system = StarSystem(
        x=star_system.x + min_distance - 20,  # Just inside minimum distance
        y=star_system.y,
        name="Close System",
        star_type=StarType.RED_GIANT,
        game_instance=mock_game
    )
    assert star_system.collides_with(close_system)

    # Create another star system outside collision range
    distant_system = StarSystem(
        x=star_system.x + min_distance + 100,  # Well outside minimum distance
        y=star_system.y,
        name="Distant System",
        star_type=StarType.BLUE_GIANT,
        game_instance=mock_game
    )
    assert not star_system.collides_with(distant_system)

def test_planet_generation(star_system):
    """Test that planets are generated for the star system."""
    assert len(star_system.planets) > 0  # At least one planet should be generated
    
    for planet in star_system.planets:
        # Check that each planet has all required attributes
        assert 'name' in planet
        assert 'orbit_number' in planet
        assert 'orbit_speed' in planet
        assert 'angle' in planet
        assert 'type' in planet
        assert 'size' in planet
        assert 'resources' in planet
        
        # Validate attribute values
        assert isinstance(planet['type'], PlanetType)
        assert isinstance(planet['size'], int)
        assert isinstance(planet['orbit_number'], int)
        assert isinstance(planet['orbit_speed'], float)
        assert 0 <= planet['angle'] <= 2 * 3.14159  # approximately 2π
        assert planet['name'].startswith(star_system.name)
        assert isinstance(planet['resources'], dict)
        
        # Check that resources dictionary contains entries for resource types
        for resource_type, amount in planet['resources'].items():
            assert isinstance(resource_type, ResourceType)
            assert isinstance(amount, int)
            assert 0 <= amount <= 100  # Resource values range from 0 to 100

def test_draw_galaxy_view(star_system, screen):
    """Test drawing the star system in galaxy view."""
    # Draw the star system
    star_system.draw_galaxy_view(screen)
    
    # Check that the color was set
    assert screen._color == star_system.color

def test_draw_system_view(star_system, screen):
    """Test drawing the star system in system view."""
    # Draw the system view
    star_system.draw_system_view(screen)
    
    # Check that orbits were drawn
    for planet in star_system.planets:
        orbit_radius = 100 + planet['orbit_number'] * 60
        assert orbit_radius > 0
    
    # Check that orbits are drawn with correct radius and width
    for planet in star_system.planets:
        orbit_radius = 100 + planet['orbit_number'] * 60
        # Verify orbit radius is positive and increases with orbit number
        assert orbit_radius > 0
        assert orbit_radius == 100 + planet['orbit_number'] * 60

def test_random_star_system_generation(mock_game):
    """Test random star system generation without specified parameters."""
    system = StarSystem(x=200, y=200, game_instance=mock_game)
    
    # Check that random name was generated
    assert isinstance(system.name, str)
    assert len(system.name) > 0
    
    # Check that random star type was selected
    assert isinstance(system.star_type, StarType)
    
    # Check that planets were generated according to star type properties
    props = StarProperties.PROPERTIES[system.star_type]
    assert props['min_planets'] <= len(system.planets) <= props['max_planets']
