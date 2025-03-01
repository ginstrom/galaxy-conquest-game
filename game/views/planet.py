"""
Planet view module for rendering detailed planet information and interactions.

This module handles the detailed visualization of individual planets, including
their properties, resources, and interactive elements.
"""

import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GRAY
from game.enums import GameState
from game.properties import PlanetProperties
from game.logging_config import get_logger
from game.views.infopanel import PlanetViewInfoPanel
from game.views.hover_utils import check_hover, is_within_circle

class PlanetView:
    """
    Handles rendering of the detailed planet view.
    
    This class manages the visualization of individual planets, showing their
    properties, resources, and providing interaction capabilities.
    """
    
    def __init__(self, game):
        """
        Initialize the planet view.
        
        Args:
            game: The main game instance
        """
        self.logger = get_logger(__name__)
        self.logger.info("Initializing PlanetView")
        self.game = game
        self.panel = PlanetViewInfoPanel(game)
        self.available_width = SCREEN_WIDTH - self.panel.panel_width
        self.center_x = self.available_width // 2
        self.center_y = SCREEN_HEIGHT // 2
        
        # Font setup
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 36)
    
    def handle_keydown(self, event):
        """
        Handle key press in the planet view.
        
        Args:
            event: The pygame key event
        """
        self.logger.debug(f"Key pressed in planet view: {pygame.key.name(event.key)}")
        
        if event.key == pygame.K_ESCAPE:
            self.logger.info("ESC pressed - transitioning from PLANET to SYSTEM view")
            # Change state immediately
            self.game.selected_planet = None
            self.game.to_state(GameState.PLANET, GameState.SYSTEM)

    def handle_click(self, pos):
        """
        Handle mouse click in the planet view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        self.logger.debug(f"Mouse click at position {pos}")
        
        # Check if click is within the info panel
        if pos[0] > self.available_width:
            self.logger.debug("Click in info panel area, ignoring")
            return
        
        # Change state immediately
        self.game.selected_planet = None
        self.game.to_state(GameState.PLANET, GameState.SYSTEM)

    def handle_right_click(self, pos):
        """
        Handle right mouse click in the planet view.
        
        Args:
            pos (tuple): The (x, y) position of the mouse click
        """
        self.logger.debug(f"Right mouse click at position {pos}")
        
        # Check if click is within the info panel
        if pos[0] > self.available_width:
            self.logger.debug("Right click in info panel area, ignoring")
            return
        
        # Change state immediately
        self.game.selected_planet = None
        self.game.to_state(GameState.PLANET, GameState.SYSTEM)
    
    def update(self):
        """
        Update the planet view state, including checking for hover.
        
        This method should be called each frame to update the hover state.
        """
        # In the planet view, we don't need to track hover state for the planet
        # since we're already viewing it in detail. This method is included
        # for consistency with other views.
                
        pass
    
    def draw(self, screen):
        """
        Draw the detailed planet view.
        
        Renders the planet with its name, type, and a large visualization.
        Uses the same style as system view for consistency.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Update hover state (for consistency with other views)
        self.update()
        planet = self.game.selected_planet
        if not planet:
            self.logger.warning("No planet selected to draw")
            self.game.debug.add("** No planet selected to draw **")
            return
            
        # Draw background
        self.game.background.draw_system_background(screen)
        
        # Draw planet name with shadow
        name_shadow = self.title_font.render(planet['name'], True, GRAY)
        name_text = self.title_font.render(planet['name'], True, WHITE)
        
        shadow_rect = name_shadow.get_rect(center=(self.center_x + 1, self.center_y//2 + 1))
        text_rect = name_text.get_rect(center=(self.center_x, self.center_y//2))
        
        screen.blit(name_shadow, shadow_rect)
        screen.blit(name_text, text_rect)
        
        # Draw planet type below name
        type_text = self.info_font.render(planet['type'].value, True, 
                                        PlanetProperties.PROPERTIES[planet['type']]['color'])
        type_rect = type_text.get_rect(center=(self.center_x, self.center_y//2 + 40))
        screen.blit(type_text, type_rect)
        
        # Draw the planet
        planet_color = PlanetProperties.PROPERTIES[planet['type']]['color']
        planet_size = planet['size'] * 4  # Make planet appear larger in detail view
        pygame.draw.circle(screen, planet_color, 
                         (self.center_x, self.center_y), 
                         planet_size)
        
        # Draw info panel
        self.panel.draw(screen)
