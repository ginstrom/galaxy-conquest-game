"""
System view module for rendering a star system and its orbiting planets.
"""

import pygame
from game.debug import debug
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.enums import GameState
from game.logging_config import get_logger

class SystemView:
    """Handles rendering of the system view including planets and info panel."""
    
    def __init__(self, game):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing SystemView")
        self.game = game
        self.available_width = SCREEN_WIDTH - game.info_panel_width
        self.center_x = self.available_width // 2
        self.center_y = SCREEN_HEIGHT // 2
    
    def handle_keydown(self, event):
        """
        Handle key press in the system view.
        
        Args:
            event: The pygame key event
        """
        self.logger.debug(f"Key pressed in system view: {pygame.key.name(event.key)}")
    
    def handle_click(self, pos):
        """
        Handle mouse click in the system view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        self.logger.debug(f"Mouse click at position {pos}")
        
        if not self.game.selected_system:
            self.logger.debug("No system selected, ignoring click")
            return
        
        for planet in self.game.selected_system.planets:
            x = planet['x']
            y = planet['y']
            
            # Check if click is within planet's radius
            dx = pos[0] - x
            dy = pos[1] - y
            if dx * dx + dy * dy <= planet['size'] * planet['size']:
                self.logger.info(f"Selected planet: {planet.get('name', 'Unnamed')}")
                self.game.selected_planet = planet
                # Change state immediately
                self.logger.info("Transitioning to PLANET view")
                self.game.state = GameState.PLANET
                break
    
    def draw(self, screen):
        """
        Draw the system view showing planets orbiting the selected star.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw background
        self.game.background.draw_system_background(screen)
        
        if self.game.selected_system:
            # Draw the system
            self.game.selected_system.draw_system_view(screen)
            
            # Draw info panel
            self.game.draw_info_panel(screen)
