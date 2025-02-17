"""
Menu system for Galaxy Conquest.

This module implements a flexible menu system with:
- Support for keyboard and mouse input
- Visual feedback for selected and disabled items
- Semi-transparent overlay for better visibility
- Cached text rendering for performance
- Customizable appearance including titles and item spacing
"""

import pygame
from .constants import WHITE, GRAY, BLACK
from .resources import ResourceManager

class MenuItem:
    """
    Represents a single menu item with text, associated action, and state.
    
    Each menu item can be enabled/disabled and selected/unselected.
    When selected and enabled, a visual indicator appears next to the item.
    
    Args:
        text (str): The text to display for this menu item
        action (callable): Function to call when this item is activated
        enabled (bool): Whether this item can be selected/activated
    """
    
    def __init__(self, text, action, enabled=True):
        self.text = text
        self.action = action
        self.enabled = enabled
        self.selected = False

    def draw(self, screen, pos, resource_manager, font_size=48):
        """
        Draw the menu item with appropriate visual state.
        
        Uses the ResourceManager's text cache for efficient text rendering.
        Draws a selection indicator (circle) when the item is selected.
        
        Args:
            screen: Pygame surface to draw on
            pos (tuple): (x, y) position to draw at
            resource_manager: ResourceManager instance for text rendering
            font_size (int): Size of the font to use
        """
        color = WHITE if self.enabled else GRAY
        text_surface = resource_manager.text_cache.get_text(
            self.text, 
            font_size, 
            color
        )
        
        if self.selected and self.enabled:
            # Draw selection indicator
            pygame.draw.circle(
                screen, 
                WHITE, 
                (pos[0] - 20, pos[1] + text_surface.get_height()//2), 
                5
            )
        
        screen.blit(text_surface, pos)

class Menu:
    """
    Manages a collection of menu items with navigation and selection handling.
    
    Features:
    - Semi-transparent background overlay
    - Bordered menu container
    - Optional title
    - Keyboard (arrow keys, enter) and mouse input
    - Visual feedback for selection
    
    Args:
        items (list): List of MenuItem objects to display
        title (str): Optional title to display above menu items
    """
    
    def __init__(self, items, title="", resource_manager=None):
        self.items = items
        self.title = title
        self.selected_index = 0
        if resource_manager is None:
            import pygame
            resource_manager = ResourceManager(pygame, pygame.font, pygame.mixer, pygame.display)
        self.resource_manager = resource_manager
        self.screen = None  # Will be set when drawing
        
        # Default font sizes
        self.title_size = 64
        self.item_size = 48

    def draw(self, screen):
        """
        Draw the complete menu with background, border, title, and items.
        
        Creates a semi-transparent overlay for the entire screen and a
        darker menu background. Draws a border around the menu area and
        positions all items with consistent spacing.
        
        Args:
            screen: Pygame surface to draw on
        """
        self.screen = screen

        # Create a semi-transparent layer over the whole screen
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # Semi-transparent black overlay
        screen.blit(overlay, (0, 0))

        # Calculate menu rectangle dimensions
        menu_width = 400
        menu_height = len(self.items) * 60 + 150  # Adjust for title and spacing
        menu_x = (screen.get_width() - menu_width) // 2
        menu_y = 50

        # Draw menu background with alpha
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((0, 0, 0, 180))  # Semi-transparent black background
        screen.blit(menu_surface, (menu_x, menu_y))

        # Draw border
        border_color = (255, 255, 255)  # White border
        pygame.draw.rect(screen, border_color, (menu_x, menu_y, menu_width, menu_height), 5)

        # Draw title if exists
        if self.title:
            title_surface = self.resource_manager.text_cache.get_text(
                self.title,
                self.title_size,
                WHITE
            )
            title_rect = title_surface.get_rect(
                center=(screen.get_width() // 2, menu_y + 50)
            )
            screen.blit(title_surface, title_rect)

        # Draw menu items
        start_y = menu_y + 100
        spacing = 60
        for i, item in enumerate(self.items):
            item.selected = (i == self.selected_index)
            pos = (screen.get_width() // 2 - 100, start_y + i * spacing)
            item.draw(screen, pos, self.resource_manager, self.item_size)

    def handle_input(self, event):
        """
        Handle keyboard and mouse input for menu navigation and selection.
        
        Supports:
        - Up/Down arrow keys for navigation
        - Enter key for selection
        - Mouse click for direct item selection
        
        Args:
            event: Pygame event to process
            
        Returns:
            Result of the selected item's action if activated, None otherwise
        """
        if not self.screen:  # Guard against handle_input being called before draw
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                action = self.items[self.selected_index].action
                if self.items[self.selected_index].enabled and action:
                    return action()

        # Mouse input handling
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculate menu layout dimensions (must match draw() calculations)
            menu_width = 400  # Width of menu background
            menu_height = len(self.items) * 60 + 150  # Adjust for title and spacing
            menu_x = (self.screen.get_width() - menu_width) // 2
            menu_y = 50
            start_y = menu_y + 100  # Aligns with item drawing logic in draw()
            spacing = 60

            # Check each menu item's bounds for mouse collision
            for i, item in enumerate(self.items):
                # Create collision rectangle for each item
                item_rect = pygame.Rect(
                    self.screen.get_width() // 2 - 100,  # Match item drawing position
                    start_y + i * spacing,  # Item y position
                    200,  # Width to match text surface width
                    spacing  # Height matches spacing between items
                )
                
                if item_rect.collidepoint(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and item.enabled:
                        self.selected_index = i
                        if item.action:
                            return item.action()
                    elif event.type == pygame.MOUSEMOTION:
                        self.selected_index = i
        return None
