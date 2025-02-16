"""
Planet view module for rendering detailed planet information and interactions.
"""

from game.debug import debug
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game.enums import GameState

class PlanetView:
    """Handles rendering of the detailed planet view."""
    
    def __init__(self, game):
        self.game = game
    
    def handle_click(self, pos):
        """
        Handle mouse click in the planet view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        pass  # Currently no click handling in planet view
    
    def draw(self, screen):
        """
        Draw the detailed planet view.
        
        Currently uses debug output to display planet information while the
        full visualization is under development.
        
        Args:
            screen: The pygame surface to draw on
        """
        if self.game.selected_planet:
            debug(f"Planet Name: {self.game.selected_planet['name']}")
            debug(f"Planet Type: {self.game.selected_planet['type'].value}")
            debug(f"Size: {self.game.selected_planet['size']}")
            debug(f"Orbit Number: {self.game.selected_planet['orbit_number']}")
            debug("Resources:")
            for resource in self.game.selected_planet['resources']:
                debug(f"  {resource['type'].value}: {resource['amount']}")
