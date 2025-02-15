"""Tests for the StarSystem class."""
import pytest
import pygame
from game.star_system import StarSystem
from game.enums import StarType, PlanetType
from game.constants import WHITE, GRAY
from game.properties import StarProperties

# Initialize pygame for testing
pygame.init()

@pytest.fixture
def star_system():
    """Create a basic star system for testing."""
    return StarSystem(x=100, y=100, name="Test System", star_type=StarType.MAIN_SEQUENCE)

@pytest.fixture
def screen():
    """Create a pygame screen for testing."""
    return pygame.Surface((800, 600))

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

def test_star_system_collision(star_system):
    """Test collision detection between star systems."""
    # Create another star system close to the first one
    other_system = StarSystem(x=101, y=101, name="Other System", star_type=StarType.RED_GIANT)
    assert star_system.collides_with(other_system)

    # Create another star system far from the first one
    distant_system = StarSystem(x=1000, y=1000, name="Distant System", star_type=StarType.BLUE_GIANT)
    assert not star_system.collides_with(distant_system)

    # Test exact minimum distance
    size_sum = star_system.size + other_system.size
    min_distance = size_sum * 3
    # Test slightly beyond minimum distance
    exact_system = StarSystem(
        x=star_system.x + min_distance + 1,  # Add 1 to be just beyond minimum
        y=star_system.y,
        name="Beyond Minimum System"
    )
    assert not star_system.collides_with(exact_system)

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
        assert isinstance(planet['resources'], list)

def test_draw_galaxy_view(star_system, screen):
    """Test drawing the star system in galaxy view."""
    # Initial screen state
    initial_color = screen.get_at((star_system.x, star_system.y))
    
    # Draw the star system
    star_system.draw_galaxy_view(screen)
    
    # Check that the star was drawn (pixel color changed)
    final_color = screen.get_at((star_system.x, star_system.y))
    assert initial_color != final_color
    assert final_color == star_system.color
    
    # Check that the name was drawn (pixel color changed below star)
    name_pos = (star_system.name_rect.centerx, star_system.name_rect.centery)
    assert screen.get_at(name_pos) != initial_color

def test_draw_system_view(star_system, screen):
    """Test drawing the star system in system view."""
    # Initial screen state
    center_x = (screen.get_width() - 300) // 2  # Accounting for panel width
    center_y = screen.get_height() // 2
    initial_color = screen.get_at((center_x, center_y))
    
    # Draw the system view
    star_system.draw_system_view(screen)
    
    # Check that the star was drawn (center pixel color changed)
    final_color = screen.get_at((center_x, center_y))
    assert initial_color != final_color
    assert final_color == star_system.color
    
    # Check that planets were drawn
    for planet in star_system.planets:
        if 'x' in planet and 'y' in planet:
            planet_pos = (int(planet['x']), int(planet['y']))
            if (0 <= planet_pos[0] < screen.get_width() and 
                0 <= planet_pos[1] < screen.get_height()):
                assert screen.get_at(planet_pos) != initial_color

def test_random_star_system_generation():
    """Test random star system generation without specified parameters."""
    system = StarSystem(x=200, y=200)
    
    # Check that random name was generated
    assert isinstance(system.name, str)
    assert len(system.name) > 0
    
    # Check that random star type was selected
    assert isinstance(system.star_type, StarType)
    
    # Check that planets were generated according to star type properties
    props = StarProperties.PROPERTIES[system.star_type]
    assert props['min_planets'] <= len(system.planets) <= props['max_planets']
