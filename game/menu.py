"""Menu system for Galaxy Conquest."""

import pygame
from .constants import WHITE, GRAY, BLACK
from .resources import ResourceManager

class MenuItem:
    def __init__(self, text, action, enabled=True):
        self.text = text
        self.action = action
        self.enabled = enabled
        self.selected = False

    def draw(self, screen, pos, resource_manager, font_size=48):
        """Draw menu item using ResourceManager's text cache."""
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
    def __init__(self, items, title=""):
        self.items = items
        self.title = title
        self.selected_index = 0
        self.resource_manager = ResourceManager()  # Get singleton instance
        self.screen = None  # Will be set when drawing
        
        # Default font sizes
        self.title_size = 64
        self.item_size = 48

    def draw(self, screen):
        """Draw the menu with all its items."""
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
        """Handle input events for menu navigation and selection."""
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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Match menu layout from draw()
            menu_width = 400
            menu_height = len(self.items) * 60 + 150  # Adjust for title and spacing
            menu_x = (self.screen.get_width() - menu_width) // 2
            menu_y = 50
            start_y = menu_y + 100  # Aligns with item drawing logic in draw()
            spacing = 60

            for i, item in enumerate(self.items):
                item_rect = pygame.Rect(
                    menu_x + 50,  # Offset to center items within menu background
                    start_y + i * spacing,
                    menu_width - 100,  # Matches the inner width of the menu background
                    40  # Height of each item (ensure this matches the font size)
                )
                
                if item_rect.collidepoint(mouse_pos) and item.enabled:
                    self.selected_index = i
                    if item.action:
                        return item.action()
        return None
