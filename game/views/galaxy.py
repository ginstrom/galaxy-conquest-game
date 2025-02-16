"""
Galaxy view module for rendering the galaxy map and handling galaxy-specific interactions.
"""

import pygame
from game.debug import debug
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.enums import GameState

class GalaxyView:
    """Handles rendering of the galaxy view including star systems and info panel."""
    
    def __init__(self, game):
        self.game = game
        self.galaxy_rect = pygame.Rect(
            0, 0,
            SCREEN_WIDTH - game.info_panel_width, SCREEN_HEIGHT
        )
    
    def handle_click(self, pos):
        """
        Handle mouse click in the galaxy view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        if not self.galaxy_rect.collidepoint(pos):
            return
            
        for system in self.game.star_systems:
            if system.rect.collidepoint(pos):
                self.game.selected_system = system
                self.game.state = GameState.SYSTEM
                break
    
    def draw(self, screen):
        """
        Draw the galaxy view including star systems and info panel.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw background
        self.game.background.draw_galaxy_background(screen)
        
        # Draw star systems
        for system in self.game.star_systems:
            system.draw_galaxy_view(screen)
        
        # Draw info panel
        self.game.draw_info_panel(screen)
        
        # Draw vertical line to separate info panel
        pygame.draw.line(
            screen, 
            WHITE,
            (self.galaxy_rect.right, 0),
            (self.galaxy_rect.right, SCREEN_HEIGHT)
        )
