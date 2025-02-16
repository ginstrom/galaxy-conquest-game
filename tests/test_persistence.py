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


class MockStarSystem:
    def __init__(self, x, y, name, star_type, size, color, planets):
        self.x = x
        self.y = y
        self.name = name
        self.star_type = star_type
        self.size = size
        self.color = color
        self.planets = planets


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
            {
                'name': 'Planet 1',
                'type': PlanetType.DESERT,
                'resources': [
                    {'type': ResourceType.MINERALS, 'amount': 100}
                ]
            },
            {
                'name': 'Planet 2',
                'type': PlanetType.OCEANIC,
                'resources': [
                    {'type': ResourceType.CRYSTALS, 'amount': 50}
                ]
            }
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
    
    # Save game state
    save_game_state([test_star_system], test_star_system, save_dir=save_dir)
    
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
    assert system['planets'][0]['resources'][0]['type'] == ResourceType.MINERALS


def test_save_exists_nonexistent_file(tmp_path):
    assert not save_exists(save_dir=str(tmp_path))


def test_load_game_state_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_game_state(save_dir=str(tmp_path))


def test_create_save_data_no_selected_system(test_star_system):
    result = create_save_data([test_star_system])
    assert result['selected_system'] is None
