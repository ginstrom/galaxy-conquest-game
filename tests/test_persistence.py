"""
Tests for the persistence module.
"""

import json
import os
import pytest
from datetime import datetime
from game.persistence import (
    convert_planet_data,
    create_save_data,
    save_game_state,
    load_game_state,
    save_exists
)
from game.enums import StarType, PlanetType, ResourceType


class MockPlanet:
    """Mock Planet class for testing."""
    def __init__(self, name, planet_type, resources):
        self.name = name
        self.type = planet_type
        self.resources = resources
    
    def copy(self):
        """Create a copy of the planet data."""
        return {
            'name': self.name,
            'type': self.type,
            'resources': self.resources.copy() if isinstance(self.resources, dict) else [r.copy() for r in self.resources]
        }
    
    def to_dict(self):
        """Convert planet to a dictionary for JSON serialization."""
        return self.copy()


class MockStarSystem:
    def __init__(self, x, y, name, star_type, size, color, planets):
        self.x = x
        self.y = y
        self.name = name
        self.star_type = star_type
        self.size = size
        self.color = color
        self.planets = planets
    
    def to_dict(self):
        """Convert star system to a dictionary for JSON serialization."""
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'star_type': self.star_type.name,
            'size': self.size,
            'color': self.color,
            'planets': [convert_planet_data(p) for p in self.planets]
        }


class MockEmpire:
    """Mock Empire class for testing."""
    def __init__(self, planets=None):
        self._planets = planets or []
    
    @property
    def planets(self):
        return self._planets


@pytest.fixture
def test_planet_data():
    return {
        'name': 'Test Planet',
        'type': PlanetType.DESERT,
        'resources': [
            {'type': ResourceType.MINERALS, 'amount': 100},
            {'type': ResourceType.CRYSTALS, 'amount': 50}
        ]
    }


@pytest.fixture
def test_star_system():
    return MockStarSystem(
        x=100,
        y=200,
        name='Test System',
        star_type=StarType.BLUE_GIANT,
        size=30,
        color=(100, 150, 255),
        planets=[
            MockPlanet(
                name='Planet 1',
                planet_type=PlanetType.DESERT,
                resources=[
                    {'type': ResourceType.MINERALS, 'amount': 100}
                ]
            ),
            MockPlanet(
                name='Planet 2',
                planet_type=PlanetType.OCEANIC,
                resources=[
                    {'type': ResourceType.CRYSTALS, 'amount': 50}
                ]
            )
        ]
    )


def test_convert_planet_data(test_planet_data):
    result = convert_planet_data(test_planet_data)
    
    assert result['name'] == 'Test Planet'
    assert result['type'] == 'DESERT'
    assert len(result['resources']) == 2
    assert result['resources'][0]['type'] == 'MINERALS'
    assert result['resources'][0]['amount'] == 100
    assert 'angle' in result
    assert 'orbit_speed' in result


def test_create_save_data(test_star_system):
    result = create_save_data([test_star_system], test_star_system)
    
    assert len(result['star_systems']) == 1
    system = result['star_systems'][0]
    assert system['x'] == 100
    assert system['y'] == 200
    assert system['name'] == 'Test System'
    assert system['star_type'] == 'BLUE_GIANT'
    assert system['size'] == 30
    assert system['color'] == (100, 150, 255)
    assert len(system['planets']) == 2
    assert result['selected_system'] == 'Test System'
    assert 'timestamp' in result


def test_save_and_load_game_state(test_star_system, tmp_path):
    # Use temporary directory for test
    save_dir = str(tmp_path)
    
    # Create mock empire with a planet
    mock_planet = test_star_system.planets[0]  # Use first planet from test system
    mock_empire = MockEmpire([mock_planet])
    mock_empires = [mock_empire]
    
    # Save game state
    save_game_state(
        [test_star_system], 
        test_star_system, 
        mock_empires, 
        mock_empire,  # First empire is player empire
        save_dir=save_dir
    )
    
    # Verify save file exists
    assert save_exists(save_dir=save_dir)
    
    # Load game state
    loaded_data = load_game_state(save_dir=save_dir)
    
    # Verify loaded data
    assert len(loaded_data['star_systems']) == 1
    system = loaded_data['star_systems'][0]
    assert system['name'] == 'Test System'
    assert system['star_type'] == StarType.BLUE_GIANT
    assert len(system['planets']) == 2
    assert system['planets'][0]['type'] == PlanetType.DESERT
    
    # Verify empire data
    assert 'empires' in loaded_data
    assert len(loaded_data['empires']) == 1
    assert loaded_data['empires'][0]['planets'] == ['Planet 1']  # Planet name from test_star_system
    assert loaded_data['player_empire_index'] == 0
    
    # Check if resources is a dictionary (new format) or a list (old format)
    planet_resources = system['planets'][0]['resources']
    if isinstance(planet_resources, dict):
        # New format: resources is a dictionary with ResourceType keys
        assert ResourceType.MINERALS in planet_resources
    else:
        # Old format: resources is a list of dictionaries
        assert planet_resources[0]['type'] == ResourceType.MINERALS


def test_save_exists_nonexistent_file(tmp_path):
    assert not save_exists(save_dir=str(tmp_path))


def test_load_game_state_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_game_state(save_dir=str(tmp_path))


def test_create_save_data_no_selected_system(test_star_system):
    result = create_save_data([test_star_system])
    assert result['selected_system'] is None


def test_load_game_state_without_empires(test_star_system, tmp_path):
    """Test loading a game state that doesn't have empire data (backward compatibility)."""
    save_dir = str(tmp_path)
    save_path = os.path.join(save_dir, 'autosave.json')
    
    # Create a save file without empire data
    save_data = {
        'star_systems': [
            {
                'name': test_star_system.name,
                'x': test_star_system.x,
                'y': test_star_system.y,
                'star_type': test_star_system.star_type.name,
                'size': test_star_system.size,
                'color': test_star_system.color,
                'planets': [convert_planet_data(p) for p in test_star_system.planets]
            }
        ],
        'selected_system': test_star_system.name
    }
    
    # Save directly to file
    os.makedirs(save_dir, exist_ok=True)
    with open(save_path, 'w') as f:
        json.dump(save_data, f)
    
    # Load game state
    loaded_data = load_game_state(save_dir=save_dir)
    
    # Verify loaded data has empty empire data
    assert 'empires' in loaded_data
    assert loaded_data['empires'] == []
    assert loaded_data['player_empire_index'] is None
