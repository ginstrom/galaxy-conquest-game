"""Tests for the StarSystem class."""
import pytest
import pygame
from game.star_system import StarSystem
from game.enums import StarType

# Initialize pygame for testing
pygame.init()

@pytest.fixture
def star_system():
    """Create a basic star system for testing."""
    return StarSystem(x=100, y=100, name="Test System", star_type=StarType.MAIN_SEQUENCE)

def test_star_system_initialization(star_system):
    """Test that a star system is properly initialized."""
    assert star_system.name == "Test System"
    assert star_system.x == 100
    assert star_system.y == 100
    assert star_system.star_type == StarType.MAIN_SEQUENCE
    assert isinstance(star_system.planets, list)

def test_star_system_collision(star_system):
    """Test collision detection between star systems."""
    # Create another star system close to the first one
    other_system = StarSystem(x=101, y=101, name="Other System", star_type=StarType.RED_GIANT)
    assert star_system.collides_with(other_system)

    # Create another star system far from the first one
    distant_system = StarSystem(x=1000, y=1000, name="Distant System", star_type=StarType.BLUE_GIANT)
    assert not star_system.collides_with(distant_system)

def test_planet_generation(star_system):
    """Test that planets are generated for the star system."""
    assert len(star_system.planets) > 0  # At least one planet should be generated
    for planet in star_system.planets:
        # Check that each planet has the required attributes
        assert 'name' in planet
        assert 'orbit_number' in planet
        assert 'orbit_speed' in planet
        assert 'angle' in planet
