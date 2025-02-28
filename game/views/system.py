"""
System view module for rendering a star system and its orbiting planets.
"""

import pygame
from game.debug import debug
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.enums import GameState
from game.logging_config import get_logger
from game.menu import Menu, MenuItem
from game.views.infopanel import SystemViewInfoPanel
from game.views.hover_utils import check_hover, is_within_circle


class SystemView:
    """Handles rendering of the system view including planets and info panel."""
    
    def __init__(self, game):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing SystemView")
        self.game = game
        self.panel = SystemViewInfoPanel(game)
        self.available_width = SCREEN_WIDTH - self.panel.panel_width
        self.center_x = self.available_width // 2
        self.center_y = SCREEN_HEIGHT // 2
        # In-game menu (when pressing ESC from system view)
        system_menu_items = [
            MenuItem("Resume Game", self.game.return_to_game),
            MenuItem("Galaxy View", self.game.go_to_galaxy_view),
            MenuItem("Quit to Desktop", self.game.quit_game)
        ]
        self.menu = Menu(system_menu_items, "Pause")
    
    def handle_keydown(self, event):
        """
        Handle key press in the system view.
        
        Args:
            event: The pygame key event
        """
        # escape key to open in-game menu
        if event.key == pygame.K_ESCAPE:
            self.logger.info("Opening in-game menu")
            self.game.to_state(GameState.SYSTEM, GameState.SYSTEM_MENU)
            return
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
            # Skip planets that don't have coordinates yet
            if 'x' not in planet or 'y' not in planet:
                continue
                
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
                self.game.to_state(GameState.SYSTEM, GameState.PLANET)
                break

    def handle_right_click(self, pos):
        """
        Handle right mouse click in the system view.
        
        Args:
            pos: The (x, y) position of the mouse click
        """
        self.logger.debug(f"Right mouse click at position {pos}")
        
        if not self.game.selected_system:
            self.logger.debug("No system selected, ignoring right click")
            return

        self.game.selected_planet = None
        self.game.to_state(GameState.SYSTEM, GameState.SYSTEM_MENU)
        self.logger.info("Right click: Transitioning to SYSTEM MENU view")
    
    def update(self):
        """
        Update the system view state, including checking for planet hover.
        
        This method should be called each frame to update the hover state.
        """
        # Clear hover state by default
        self.game.hovered_planet = None
        
        if not self.game.selected_system or self.game.state != GameState.SYSTEM:
            return
            
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if mouse is within the system view area (not over info panel)
        rect_check_func = lambda pos: pos[0] < self.available_width
        
        # Filter out planets without coordinates
        valid_planets = [p for p in self.game.selected_system.planets if 'x' in p and 'y' in p]
        
        # Use the common hover detection function
        self.game.hovered_planet = check_hover(
            mouse_pos,
            valid_planets,
            is_within_circle,
            rect_check_func
        )
    
    def draw(self, screen):
        """
        Draw the system view showing planets orbiting the selected star.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Update hover state
        self.update()
        
        # Draw background
        self.game.background.draw_system_background(screen)
        
        if self.game.selected_system:
            # Draw the system
            self.game.selected_system.draw_system_view(screen)
            
            # Draw info panel
            self.panel.draw(screen)
        else:
            self.logger.warning("No system selected to draw")
            self.logger.info("Transitioning to GALAXY view")
            self.game.to_state(GameState.SYSTEM, GameState.GALAXY)
        if self.game.selected_system:
            ss = self.game.selected_system
            debug(f"System: {ss.name}")
            debug(f"Planets: {len(ss.planets)}")
            debug(f"Mouse: {pygame.mouse.get_pos()}")
            if self.game.selected_planet:
                sp = self.game.selected_planet
                debug(f"Selected: {sp['name']}")
            if self.game.hovered_planet:
                hp = self.game.hovered_planet
                debug(f"Hovered: {hp['name']}")
        
        # Note: Menu drawing is now handled by the game loop
