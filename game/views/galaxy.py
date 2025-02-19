"""
Galaxy view module for rendering the galaxy map and handling galaxy-specific interactions.
"""

import pygame
from game.debug import debug
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.enums import GameState
from game.logging_config import get_logger
from game.menu import Menu, MenuItem

class GalaxyView:
    """Handles rendering of the galaxy view including star systems and info panel."""
    
    def __init__(self, game):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing GalaxyView")
        self.game = game
        self.galaxy_rect = pygame.Rect(
            0, 0,
            SCREEN_WIDTH - game.info_panel.panel_width, SCREEN_HEIGHT
        )
        # In-game menu (when pressing ESC from galaxy view)
        galaxy_menu_items = [
            MenuItem("New Game", self.game.new_game),
            MenuItem("Save", self.game.save_game),
            MenuItem("Resume Game", self.game.return_to_game),
            MenuItem("Main Menu", self.game.quit_to_main_menu),
            MenuItem("Quit to Desktop", self.game.quit_game)
        ]
        self.menu = Menu(galaxy_menu_items, "Pause")
    
    def handle_keydown(self, event):
        """
        Handle key press in the galaxy view.
        
        Args:
            event: The pygame key event
        """
        self.logger.debug(f"Key pressed in galaxy view: {pygame.key.name(event.key)}")
    
    def handle_click(self, pos):
        """
        Handle mouse click in the galaxy view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        self.logger.debug(f"Mouse click at position {pos}")
        
        if not self.galaxy_rect.collidepoint(pos):
            self.logger.debug("Click outside galaxy view area")
            return
            
        for system in self.game.star_systems:
            if system.rect.collidepoint(pos):
                self.logger.info(f"Selected star system: {system.name}")
                self.game.selected_system = system
                self.logger.info("Transitioning to SYSTEM view")
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
        
        self.game.info_panel.draw(screen)
        # Draw vertical line to separate info panel
        pygame.draw.line(
            screen, 
            WHITE,
            (self.galaxy_rect.right, 0),
            (self.galaxy_rect.right, SCREEN_HEIGHT)
        )
