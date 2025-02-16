"""
Startup view module for game initialization and main menu.

This module provides:
- Initial game menu with new game/load game options
- Background effects during startup
- Transition to galaxy view
"""

import pygame
from typing import Optional

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
        ], title="Galaxy Conquest")

    def start_new_game(self) -> bool:
        """
        Start a new game.
        
        Initializes new game state and transitions to galaxy view.
        
        Returns:
            bool: True to keep game running
        """
        # Store startup view state before transition
        self.game.view_state.store_state(
            GameState.STARTUP_MENU.value,
            {'menu_index': self.menu.selected_index}
        )
        
        # Start transition effect
        self.game.transition.start(
            GameState.STARTUP_MENU.value,
            GameState.GALAXY.value
        )
        
        # Initialize new game
        self.game.new_game()
        return True

    def load_game(self) -> bool:
        """
        Load a saved game.
        
        Attempts to load saved game state and transition to galaxy view.
        
        Returns:
            bool: True if load successful and game should continue
        """
        if self.game.load_game():
            # Store startup view state
            self.game.view_state.store_state(
                GameState.STARTUP_MENU.value,
                {'menu_index': self.menu.selected_index}
            )
            
            # Start transition to galaxy view
            self.game.transition.start(
                GameState.STARTUP_MENU.value,
                GameState.GALAXY.value
            )
            return True
        return True  # Keep game running even if load fails

    def exit_game(self) -> bool:
        """
        Exit the game.
        
        Returns:
            bool: False to signal game loop to end
        """
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

    def handle_input(self, event: pygame.event.Event) -> Optional[bool]:
        """
        Handle user input events.
        
        Args:
            event: Pygame event to process
            
        Returns:
            bool or None: False to quit game, True to continue, None if no action
        """
        return self.menu.handle_input(event)

    def restore_state(self, state_data: dict) -> None:
        """
        Restore view state from saved data.
        
        Args:
            state_data: Dictionary containing view state data
        """
        if state_data and 'menu_index' in state_data:
            try:
                index = int(state_data['menu_index'])
                if 0 <= index < len(self.menu.items):
                    self.menu.selected_index = index
            except (ValueError, TypeError):
                pass  # Keep original index on invalid data
