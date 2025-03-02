"""Unit tests for the Empire class."""
import pytest
from unittest.mock import MagicMock
from game.empire import Empire


@pytest.fixture
def mock_game():
    """Fixture providing a mock game instance."""
    return MagicMock()


@pytest.fixture
def empire(mock_game):
    """Fixture providing an Empire instance with a mock game."""
    return Empire(mock_game)


@pytest.fixture
def mock_planet():
    """Fixture providing a mock planet instance."""
    return MagicMock()


def test_empire_initialization(empire, mock_game):
    """
    Test Empire initialization.
    
    Verify:
    1. Planets list starts empty
    2. Game reference is correctly set
    """
    assert empire.planets == []
    assert empire._game == mock_game


@pytest.mark.parametrize("num_planets", [1, 2, 5, 10])
def test_add_multiple_planets(empire, num_planets):
    """
    Test adding multiple planets to the empire.
    
    Args:
        num_planets: Number of planets to add in this test case
    
    Verify:
    1. All planets are added successfully
    2. Planet count matches expected count
    3. Each planet is accessible in the planets list
    """
    planets = [MagicMock() for _ in range(num_planets)]
    for planet in planets:
        empire.add_planet(planet)
    
    assert len(empire.planets) == num_planets
    for planet in planets:
        assert planet in empire.planets


def test_add_planet(empire, mock_planet):
    """
    Test adding a planet to the empire.
    
    Verify:
    1. Planet is added to the planets list
    2. Planet count increases
    3. Planet reference is maintained
    """
    empire.add_planet(mock_planet)
    assert mock_planet in empire.planets
    assert len(empire.planets) == 1
    assert empire.planets[0] is mock_planet  # Verify exact object reference


def test_add_same_planet_twice(empire, mock_planet):
    """
    Test adding the same planet multiple times.
    
    Verify:
    1. Planet can be added multiple times (current implementation allows this)
    2. Planet count reflects all additions
    """
    empire.add_planet(mock_planet)
    empire.add_planet(mock_planet)
    assert mock_planet in empire.planets
    assert len(empire.planets) == 2
    assert empire.planets.count(mock_planet) == 2


def test_remove_existing_planet(empire, mock_planet):
    """
    Test removing an existing planet from the empire.
    
    Verify:
    1. Planet is removed from the planets list
    2. Planet count decreases
    3. Planet is completely removed
    """
    empire.add_planet(mock_planet)
    empire.remove_planet(mock_planet)
    assert mock_planet not in empire.planets
    assert len(empire.planets) == 0


def test_remove_nonexistent_planet(empire, mock_planet):
    """
    Test removing a non-existent planet from the empire.
    
    Verify:
    1. Operation doesn't raise an error
    2. Planets list remains unchanged
    3. No side effects occur
    """
    initial_planets = empire.planets.copy()
    another_mock_planet = MagicMock()
    empire.remove_planet(another_mock_planet)
    assert len(empire.planets) == 0
    assert empire.planets == initial_planets


def test_remove_planet_from_multiple(empire):
    """
    Test removing a specific planet when multiple planets exist.
    
    Verify:
    1. Multiple planets can be added
    2. Specific planet can be removed
    3. Other planets remain unchanged
    4. Order is preserved
    """
    planets = [MagicMock() for _ in range(3)]
    for planet in planets:
        empire.add_planet(planet)
    
    # Remove middle planet
    empire.remove_planet(planets[1])
    assert len(empire.planets) == 2
    assert planets[1] not in empire.planets
    assert empire.planets == [planets[0], planets[2]]  # Order preserved


@pytest.mark.parametrize("duplicate_count", [2, 3, 5])
def test_remove_duplicate_planet(empire, mock_planet, duplicate_count):
    """
    Test removing a planet that exists multiple times.
    
    Args:
        duplicate_count: Number of times to add the same planet
    
    Verify:
    1. Only one instance is removed
    2. Other instances remain
    3. Count is correctly decreased
    """
    # Add the same planet multiple times
    for _ in range(duplicate_count):
        empire.add_planet(mock_planet)
    
    # Remove once
    empire.remove_planet(mock_planet)
    assert mock_planet in empire.planets
    assert len(empire.planets) == duplicate_count - 1
    assert empire.planets.count(mock_planet) == duplicate_count - 1 