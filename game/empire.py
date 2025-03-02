"""
The Empire class is responsible for managing the empire's resources and units.

The Game class has 2 or more empires:
- The player's empire
- The enemy empire(s)

The Empire class is responsible for managing the empire's resources and units.
- Planets:
    - The empire's home planets
    - The empire's colonies
    - The empire's outposts
- Resources:
    - Empire-wide resources accumulated from the empire's planets
- Units:
    - The empire's military units
    - The empire's civilian units
"""
from game.logging_config import get_logger

logger = get_logger(__name__)


class Empire:
    def __init__(self, game):
        """Initialize an empire.
        
        Args:
            game: The main Game instance
        """
        self._game = game
        self._planets = []  # List of planets in the empire
        logger.debug("Empire initialized")
    
    @property 
    def planets(self):
        """Get list of planets in the empire."""
        return self._planets
    
    def add_planet(self, planet):
        """Add a planet to the empire.
        
        Args:
            planet: Planet instance to add
        """
        self._planets.append(planet)
        logger.debug(f"Added planet to empire: {planet}")
    
    def remove_planet(self, planet):
        """Remove a planet from the empire.
        
        Args:
            planet: Planet instance to remove
        """
        if planet in self._planets:
            self._planets.remove(planet)
            logger.debug(f"Removed planet from empire: {planet}")



