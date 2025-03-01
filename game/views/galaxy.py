"""
Galaxy view module for rendering the galaxy map and handling galaxy-specific interactions.
"""

import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.enums import GameState
from game.logging_config import get_logger
from game.menu import Menu, MenuItem
from game.views.infopanel import GalaxyViewInfoPanel
from game.views.hover_utils import check_hover, is_within_circle

class GalaxyView:
    """Handles rendering of the galaxy view including star systems and info panel."""
    
    def __init__(self, game):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing GalaxyView")
        self.game = game
        self.panel = GalaxyViewInfoPanel(game)
        self.galaxy_rect = pygame.Rect(
            0, 0,
            SCREEN_WIDTH - self.panel.panel_width, SCREEN_HEIGHT
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
        # escape key to open in-game menu
        if event.key == pygame.K_ESCAPE:
            self.logger.info("Opening in-game menu")
            self.game.to_state(GameState.GALAXY, GameState.GALAXY_MENU)
            return
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
                self.game.to_state(GameState.GALAXY, GameState.SYSTEM)
                break
    
    def handle_right_click(self, pos):
        """
        Handle right mouse click in the galaxy view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        self.logger.debug(f"Right mouse click at position {pos}")
        
        if not self.galaxy_rect.collidepoint(pos):
            self.logger.debug("Click outside galaxy view area")
            return
        
        self.game.selected_system = None
        self.game.to_state(GameState.GALAXY, GameState.GALAXY_MENU)
        self.logger.info("Right click: Transitioning to GALAXY MENU view")
    
    def update(self):
        """
        Update the galaxy view state, including checking for system hover.
        
        This method should be called each frame to update the hover state.
        Note: The actual hover detection for systems is handled in the main game loop
        for historical reasons, but this method is included for consistency with
        other views and potential future refactoring.
        """
        self.game.hovered_system = None

        mouse_pos = pygame.mouse.get_pos()

        # Only check for hover if mouse is in galaxy area
        rect_check_func = lambda pos: self.galaxy_rect.collidepoint(pos)
        self.game.hovered_system = check_hover(
            mouse_pos, 
            self.game.star_systems, 
            lambda pos, obj: obj.rect.collidepoint(pos),
            rect_check_func,
            self.game
        )
        hs = self.game.hovered_system
        # Additional debug info if hovering
        if hs:
            self.game.debug.add(f"Hovering: {hs} at {hs.x}, {hs.y}")
            self.game.debug.add(f"Mouse pos: {mouse_pos}")
            self.game.debug.add(f"System rect: {hs.rect}")

    def draw(self, screen):
        """
        Draw the galaxy view including star systems and info panel.
        
        Args:
            screen: The pygame surface to draw on
        """
        self.update()
        # Draw background
        self.game.background.draw_galaxy_background(screen)
        
        # Draw star systems
        for system in self.game.star_systems:
            system.draw_galaxy_view(screen)
        
        self.panel.draw(screen)
        # Draw vertical line to separate info panel
        pygame.draw.line(
            screen, 
            WHITE,
            (self.galaxy_rect.right, 0),
            (self.galaxy_rect.right, SCREEN_HEIGHT)
        )
        self.game.debug.add(f"Systems: {len(self.game.star_systems)}")
        self.game.debug.add(f"Mouse: {pygame.mouse.get_pos()}")
        
        # Note: Menu drawing is now handled by the game loop
