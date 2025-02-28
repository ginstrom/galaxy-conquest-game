"""
Notifications module for Galaxy Conquest.

This module contains classes and functions for displaying in-game notifications
to the user, such as save confirmations, alerts, and other temporary messages.
"""

import pygame
import pygame_gui
from game.constants import SCREEN_WIDTH


class NotificationManager:
    """
    Manages the display of temporary notifications in the game.
    
    This class is responsible for:
    - Creating and displaying notification messages
    - Timing the display duration of notifications
    - Removing notifications when they expire
    """
    
    def __init__(self, ui_manager):
        """
        Initialize the NotificationManager.
        
        Args:
            ui_manager: The pygame_gui UIManager instance to use for creating UI elements
        """
        self.ui_manager = ui_manager
        self.save_notification_time = 0
        self.save_notification_duration = 2000  # 2 seconds
        self.save_notification_label = None
    
    def draw_save_notification(self, screen):
        """
        Display a temporary notification using a Pygame GUI component when the game is saved.
        The UI label appears at the top center of the screen and is removed after 2 seconds.
        
        Args:
            screen: The pygame surface to draw on (not used directly for the notification)
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.save_notification_time < self.save_notification_duration:
            # If the notification label doesn't exist, create it using pygame_gui
            if not self.save_notification_label:
                rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 25), (200, 50))
                self.save_notification_label = pygame_gui.elements.UILabel(
                    relative_rect=rect,
                    text="Game Saved!",
                    manager=self.ui_manager,
                    object_id="#save_notification"
                )
        else:
            # If the duration has passed and the label exists, remove it
            if self.save_notification_label:
                self.save_notification_label.kill()
                self.save_notification_label = None
    
    def show_save_notification(self):
        """
        Trigger the display of a save notification.
        
        This method should be called when the game is saved to start the notification timer.
        """
        self.save_notification_time = pygame.time.get_ticks()
