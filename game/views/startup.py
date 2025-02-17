"""
Startup view module for game initialization and main menu.

This module provides:
- Initial game menu with new game/load game options
- Background effects during startup
"""

import pygame
from typing import Optional

from game.logging_config import get_logger
from game.menu import Menu, MenuItem
from game.background import BackgroundEffect
from game.persistence import save_exists
from game.enums import GameState


class StartupView:
    """
    Handles the startup/main menu view of the game.
    
    Features:
    - New game option
    - Load game option (enabled if save exists)
    - Exit option
    - Dynamic star field background
    """
    
    def __init__(self, game):
        """
        Initialize the startup view.
        
        Args:
            game: Main game instance for state management
        """
        self.logger = get_logger(__name__)
        self.logger.info("Initializing StartupView")
        self.game = game
        self.background = BackgroundEffect()
        self.create_menu()

    def create_menu(self) -> None:
        """Create the startup menu with appropriate options."""
        has_save = save_exists()  # Cache the result
        self.menu = Menu([
            MenuItem("New Game", self.start_new_game),
            MenuItem("Load Game", self.load_game, enabled=has_save),
            MenuItem("Exit", self.exit_game)
        ], title="Galaxy Conquest", resource_manager=self.game.resource_manager)

    def start_new_game(self) -> bool:
        """
        Start a new game.
        
        Returns:
            bool: True to keep game running
        """
        self.logger.info("Starting new game")
        self.game.new_game()
        return True

    def load_game(self) -> bool:
        """
        Load a saved game.
        
        Returns:
            bool: True if load successful and game should continue
        """
        self.logger.info("Attempting to load saved game")
        if self.game.load_game():
            self.logger.info("Game loaded successfully")
            return True
        self.logger.warning("Failed to load game")
        return True  # Keep game running even if load fails

    def exit_game(self) -> bool:
        """
        Exit the game.
        
        Returns:
            bool: False to signal game loop to end
        """
        self.logger.info("Exiting game from startup menu")
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the startup view.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw animated star field background
        self.background.draw_galaxy_background(screen)
        
        # Draw menu on top
        self.menu.draw(screen)

    def handle_keydown(self, event: pygame.event.Event) -> Optional[bool]:
        """
        Handle key press in the startup view.
        
        Args:
            event: The pygame key event
            
        Returns:
            bool or None: False to quit game, True to continue, None if no action
        """
        self.logger.debug(f"Key pressed in startup view: {pygame.key.name(event.key)}")
        result = self.menu.handle_input(event)
        if result is not None:
            self.logger.debug(f"Menu action result: {result}")
        return result

    def handle_click(self, pos: tuple) -> Optional[bool]:
        """
        Handle mouse click in the startup view.
        
        Args:
            pos: The (x, y) position of the mouse click
            
        Returns:
            bool or None: False to quit game, True to continue, None if no action
        """
        self.logger.debug(f"Mouse click at position {pos}")
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})
        result = self.menu.handle_input(event)
        if result is not None:
            self.logger.debug(f"Menu action result: {result}")
        return result
