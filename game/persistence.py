"""
Persistence module for saving and loading game state.

This module handles saving and loading game state to/from JSON files.
It provides functionality to:
- Save game state to JSON files
- Load game state from JSON files
- Convert game objects to/from JSON-serializable format
"""

import json
import os
from datetime import datetime
import random
import math
from typing import Dict, List, Optional, Any

from game.enums import StarType, PlanetType, ResourceType
from game.planet import Planet
from game.logging_config import get_logger

logger = get_logger(__name__)


def convert_planet_data(planet) -> Dict[str, Any]:
    """
    Convert planet data to JSON-serializable format.
    
    Args:
        planet: Planet object or dictionary containing planet data
        
    Returns:
        Dict containing JSON-serializable planet data
    """
    # If planet is a Planet object, convert it to a dictionary first
    if hasattr(planet, 'to_dict'):
        planet_dict = planet.to_dict()
    else:
        planet_dict = planet.copy()
    
    # Create a copy to avoid modifying the original
    planet_copy = planet_dict.copy()
    
    # Convert PlanetType enum
    if isinstance(planet_dict['type'], PlanetType):
        planet_copy['type'] = planet_dict['type'].name
    
    # Convert resources data
    resources_copy = []
    if isinstance(planet_dict['resources'], dict):
        # Convert from dict format to list format for JSON serialization
        for resource_type, amount in planet_dict['resources'].items():
            resource_copy = {
                'type': resource_type.name if isinstance(resource_type, ResourceType) else resource_type,
                'amount': amount
            }
            resources_copy.append(resource_copy)
    else:
        # Already in list format
        for resource in planet_dict['resources']:
            resource_copy = resource.copy()
            # Convert ResourceType enum if it's an enum
            if isinstance(resource['type'], ResourceType):
                resource_copy['type'] = resource['type'].name
            resources_copy.append(resource_copy)
    
    planet_copy['resources'] = resources_copy
    
    # Ensure angle and orbit_speed are included
    if 'angle' not in planet_copy:
        planet_copy['angle'] = random.uniform(0, 2 * math.pi)
    if 'orbit_speed' not in planet_copy:
        planet_copy['orbit_speed'] = random.uniform(0.2, 0.5)
    
    return planet_copy


def create_save_data(star_systems: List[Any], selected_system: Optional[Any] = None) -> Dict[str, Any]:
    """
    Create a JSON-serializable dictionary of game state data.
    
    Args:
        star_systems: List of StarSystem objects
        selected_system: Currently selected StarSystem object or None
        
    Returns:
        Dict containing JSON-serializable game state data
    """
    return {
        'star_systems': [
            {
                'x': system.x,
                'y': system.y,
                'name': system.name,
                'star_type': system.star_type.name,
                'size': system.size,
                'color': system.color,
                'planets': [convert_planet_data(p) for p in system.planets]
            }
            for system in star_systems
        ],
        'selected_system': selected_system.name if selected_system else None,
        'timestamp': datetime.now().isoformat()
    }


def save_game_state(star_systems, selected_system=None, empires=None, player_empire=None, save_dir='saves', filename='autosave.json'):
    """Save the current game state to a JSON file.
    
    Args:
        star_systems (list): List of StarSystem objects
        selected_system (StarSystem, optional): Currently selected system
        empires (list, optional): List of Empire objects
        player_empire (Empire, optional): Reference to player's empire
        save_dir (str, optional): Directory to save in. Defaults to 'saves'.
        filename (str, optional): Name of save file. Defaults to 'autosave.json'.
    """
    logger.info(f"Saving game state to {filename}")
    
    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Convert star systems to serializable format
    systems_data = []
    for system in star_systems:
        if hasattr(system, 'to_dict'):
            system_data = system.to_dict()
        else:
            system_data = {
                'name': system.name,
                'x': system.x,
                'y': system.y,
                'size': system.size,
                'star_type': system.star_type.name,
                'color': list(system.color),
                'planets': [convert_planet_data(p) for p in system.planets]
            }
        systems_data.append(system_data)
    
    # Convert empires to serializable format
    empires_data = []
    player_empire_index = None
    
    if empires:
        for i, empire in enumerate(empires):
            empire_data = {
                'planets': [planet.name for planet in empire.planets]  # Store planet references by name
            }
            empires_data.append(empire_data)
            
            # Track which empire is the player's
            if empire == player_empire:
                player_empire_index = i
    
    # Create save data structure
    save_data = {
        'star_systems': systems_data,
        'selected_system': selected_system.name if selected_system else None,
        'empires': empires_data,
        'player_empire_index': player_empire_index
    }
    
    # Save to file
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'w') as f:
        json.dump(save_data, f)
    
    logger.info("Game state saved successfully")


def load_game_state(save_dir: str = 'saves', filename: str = 'autosave.json') -> Dict[str, Any]:
    """Load game state from a JSON file.
    
    Args:
        save_dir (str, optional): Directory to load from. Defaults to 'saves'.
        filename (str, optional): Name of save file. Defaults to 'autosave.json'.
    
    Returns:
        dict: Loaded game state data
    
    Raises:
        FileNotFoundError: If save file doesn't exist
        json.JSONDecodeError: If save file is invalid JSON
    """
    logger.info(f"Loading game state from {filename}")
    
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'r') as f:
        save_data = json.load(f)
    
    # Convert star systems data
    for system in save_data['star_systems']:
        # Convert star type string to enum
        system['star_type'] = StarType[system['star_type']]
        
        # Convert planets list
        converted_planets = []
        
        for planet_dict in system['planets']:
            # Convert enum strings to enum types first
            planet_dict['type'] = PlanetType[planet_dict['type']]
            
            # Convert resources enum strings to enum types
            for resource in planet_dict['resources']:
                resource['type'] = ResourceType[resource['type']]

            # Ensure angle and orbit_speed are included
            if 'angle' not in planet_dict:
                planet_dict['angle'] = random.uniform(0, 2 * math.pi)
            if 'orbit_speed' not in planet_dict:
                planet_dict['orbit_speed'] = random.uniform(0.2, 0.5)
                
            # Ensure size and orbit_number are included
            if 'size' not in planet_dict:
                planet_dict['size'] = random.randint(10, 30)  # Default size range
            if 'orbit_number' not in planet_dict:
                # If we don't have orbit_number, use the index in the list
                planet_dict['orbit_number'] = system['planets'].index(planet_dict) + 1

            # Create a Planet object from the dictionary
            planet = Planet.from_dict(planet_dict)
            converted_planets.append(planet)

        # Replace the list of planet dictionaries with Planet objects
        system['planets'] = converted_planets
    
    # Add empty empires list if not present in save data
    if 'empires' not in save_data:
        save_data['empires'] = []
        save_data['player_empire_index'] = None
    
    return save_data


def save_exists(save_dir: str = 'saves', filename: str = 'autosave.json') -> bool:
    """
    Check if a save file exists.
    
    Args:
        save_dir: Directory to check for save file
        filename: Name of save file
        
    Returns:
        bool: True if save file exists, False otherwise
    """
    save_path = os.path.join(save_dir, filename)
    return os.path.exists(save_path)
