"""
Planet module for Galaxy Conquest.

This module defines the Planet class, which represents a planet in the game.
Each planet has properties such as type, size, resources, and orbital characteristics.
"""

import random
from .enums import PlanetType, ResourceType
from .properties import PlanetProperties

class Planet:
    """
    Represents a planet in the game with its properties and resources.
    
    A planet has a type, size, resources, and orbital characteristics.
    It can be rendered in both the system view and the planet view.
    
    Args:
        name (str): The name of the planet
        planet_type (PlanetType): The type of the planet
        size (int): The size of the planet
        orbit_number (int): The orbit number of the planet
        angle (float, optional): The angle of the planet in its orbit
        orbit_speed (float, optional): The speed of the planet in its orbit
        resources (dict, optional): A dictionary of resources, with resource types as keys and amounts as values
    """
    
    def __init__(self, name, planet_type, size, orbit_number, 
                 angle=None, orbit_speed=None, resources=None):
        """
        Initialize a planet with the given properties.
        
        Args:
            name (str): The name of the planet
            planet_type (PlanetType): The type of the planet
            size (int): The size of the planet
            orbit_number (int): The orbit number of the planet
            angle (float, optional): The angle of the planet in its orbit
            orbit_speed (float, optional): The speed of the planet in its orbit
            resources (dict, optional): A dictionary of resources, with resource types as keys and amounts as values
        """
        self.name = name
        self.type = planet_type
        self.size = size
        self.orbit_number = orbit_number
        self.angle = angle if angle is not None else random.uniform(0, 2 * 3.14159)
        self.orbit_speed = orbit_speed if orbit_speed is not None else random.uniform(0.2, 0.5)
        self.resources = resources if resources is not None else {}
        
        # Position in system view (set dynamically)
        self.x = None
        self.y = None
    
    @classmethod
    def from_dict(cls, planet_dict):
        """
        Create a Planet instance from a dictionary.
        
        This method is useful for converting existing planet dictionaries
        to Planet objects during the transition to the class-based approach.
        
        Args:
            planet_dict (dict): A dictionary containing planet properties
            
        Returns:
            Planet: A new Planet instance with properties from the dictionary
        """
        planet = cls(
            name=planet_dict['name'],
            planet_type=planet_dict['type'],
            size=planet_dict['size'],
            orbit_number=planet_dict['orbit_number'],
            angle=planet_dict.get('angle'),
            orbit_speed=planet_dict.get('orbit_speed')
        )
        
        # Copy resources
        resources = planet_dict.get('resources', {})
        
        # Convert from old list format to new dict format if needed
        if isinstance(resources, list):
            resources_dict = {}
            for resource in resources:
                resources_dict[resource['type']] = resource['amount']
            planet.resources = resources_dict
        else:
            planet.resources = resources
        
        # Copy position if available
        if 'x' in planet_dict and 'y' in planet_dict:
            planet.x = planet_dict['x']
            planet.y = planet_dict['y']
        
        return planet
    
    def to_dict(self):
        """
        Convert the Planet object to a dictionary.
        
        This method is useful for serialization and for compatibility
        with code that still expects planet dictionaries.
        
        Returns:
            dict: A dictionary containing the planet's properties
        """
        planet_dict = {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'orbit_number': self.orbit_number,
            'angle': self.angle,
            'orbit_speed': self.orbit_speed,
            'resources': self.resources
        }
        
        # Include position if available
        if self.x is not None and self.y is not None:
            planet_dict['x'] = self.x
            planet_dict['y'] = self.y
        
        return planet_dict
    
    @classmethod
    def generate(cls, star_name, orbit_number):
        """
        Generate a random planet for the given star system.
        
        Args:
            star_name (str): The name of the star system
            orbit_number (int): The orbit number for the planet
            
        Returns:
            Planet: A new Planet instance with random properties
        """
        planet_type = PlanetProperties.get_random_type()
        props = PlanetProperties.PROPERTIES[planet_type]
        
        size = random.randint(props['min_size'], props['max_size'])
        resources = PlanetProperties.generate_resources(planet_type)
        name = f"{star_name} {orbit_number}"
        
        return cls(
            name=name,
            planet_type=planet_type,
            size=size,
            orbit_number=orbit_number,
            resources=resources
        )
    
    def __getitem__(self, key):
        """
        Support dictionary-like access for backward compatibility.
        
        This method allows code that expects a planet dictionary to
        continue working with Planet objects.
        
        Args:
            key (str): The key to access
            
        Returns:
            The value associated with the key
            
        Raises:
            KeyError: If the key is not found
        """
        if key == 'name':
            return self.name
        elif key == 'type':
            return self.type
        elif key == 'size':
            return self.size
        elif key == 'orbit_number':
            return self.orbit_number
        elif key == 'angle':
            return self.angle
        elif key == 'orbit_speed':
            return self.orbit_speed
        elif key == 'resources':
            return self.resources
        elif key == 'x':
            return self.x
        elif key == 'y':
            return self.y
        else:
            raise KeyError(f"Planet has no attribute '{key}'")
    
    def __contains__(self, key):
        """
        Support the 'in' operator for backward compatibility.
        
        This method allows code that expects a planet dictionary to
        continue working with Planet objects.
        
        Args:
            key (str): The key to check
            
        Returns:
            bool: True if the key exists, False otherwise
        """
        return key in ['name', 'type', 'size', 'orbit_number', 
                       'angle', 'orbit_speed', 'resources', 'x', 'y']
