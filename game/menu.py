"""
Menu system for Galaxy Conquest.

This module implements a flexible menu system with:
- Support for keyboard and mouse input using pygame_gui
- Visual feedback for selected and disabled items
- Semi-transparent overlay for better visibility
- Customizable appearance including titles and item spacing
"""

import pygame
import pygame_gui
from .constants import WHITE, GRAY, BLACK
from .resources import ResourceManager
from .logging_config import get_logger

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
        self.button = None  # Will be set when added to a menu
        self.logger = get_logger(__name__)

    def create_button(self, ui_manager, container, relative_rect):
        """
        Create a pygame_gui UIButton for this menu item.
        
        Args:
            ui_manager: The pygame_gui UIManager instance
            container: The container to add the button to
            relative_rect: The position and size of the button
        """
        self.button = pygame_gui.elements.UIButton(
            relative_rect=relative_rect,
            text=self.text,
            manager=ui_manager,
            container=container,
            object_id=f"#menu_item_{self.text.replace(' ', '_').lower()}"
        )
        
        # Set enabled state
        if not self.enabled:
            self.button.disable()
        
        return self.button

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
        self.logger = get_logger(__name__)
        self.visible = False  # Track if the menu is visible
        
        if resource_manager is None:
            import pygame
            resource_manager = ResourceManager(pygame, pygame.font, pygame.mixer, pygame.display)
        self.resource_manager = resource_manager
        
        # UI elements
        self.ui_manager = None
        self.panel = None
        self.title_label = None
        self.buttons = []
        
        # Default font sizes (kept for compatibility)
        self.title_size = 64
        self.item_size = 48
        
        # Flag to track if the menu has been initialized
        self.initialized = False
        self.screen = None

    def initialize(self, screen, ui_manager=None):
        """
        Initialize the menu UI elements.
        
        Args:
            screen: Pygame surface to draw on
            ui_manager: Optional UIManager to use (will create one if not provided)
        """
        self.screen = screen
        
        # Use provided UI manager or create a new one
        if ui_manager is None:
            self.ui_manager = pygame_gui.UIManager(
                (screen.get_width(), screen.get_height())
            )
        else:
            self.ui_manager = ui_manager
        
        # Calculate menu dimensions
        menu_width = 400
        menu_height = len(self.items) * 60 + 150  # Adjust for title and spacing
        menu_x = (screen.get_width() - menu_width) // 2
        menu_y = 50
        
        # Clean up any existing UI elements
        if self.panel:
            self.panel.kill()
            self.panel = None
            self.buttons = []
            self.title_label = None
        
        # Create panel
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(menu_x, menu_y, menu_width, menu_height),
            manager=self.ui_manager,
            object_id="#menu_panel"
        )
        
        # Add title if exists
        if self.title:
            title_height = 50
            self.title_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 10, menu_width, title_height),
                text=self.title,
                manager=self.ui_manager,
                container=self.panel,
                object_id="#menu_title"
            )
            
            # Add a separator line
            pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(20, title_height + 20, menu_width - 40, 2),
                manager=self.ui_manager,
                container=self.panel,
                object_id="#menu_separator"
            )
        
        # Add menu items
        start_y = 70 if self.title else 20
        spacing = 60
        button_width = 300
        button_height = 50
        
        for i, item in enumerate(self.items):
            button_rect = pygame.Rect(
                (menu_width - button_width) // 2,
                start_y + i * spacing,
                button_width,
                button_height
            )
            
            button = item.create_button(
                self.ui_manager,
                self.panel,
                button_rect
            )
            
            self.buttons.append(button)
        
        # Set initial selection
        self.set_selected(self.selected_index)
        self.initialized = True
        
        # Panel is initially hidden
        self.visible = False
        self.hide()
        
        self.logger.debug("Menu initialized with pygame_gui elements")

    def set_selected(self, index):
        """
        Set the selected menu item.
        
        Args:
            index (int): Index of the item to select
        """
        # Ensure index is valid
        if index < 0 or index >= len(self.items):
            return
            
        # Update selected index
        self.selected_index = index
        
        # Update visual selection state if initialized
        if self.initialized:
            # We can't visually highlight the button in pygame_gui,
            # but we can track which one is selected for keyboard navigation
            pass

    def show(self):
        """Show the menu panel."""
        if self.initialized and self.panel:
            self.panel.show()
            self.visible = True
            self.logger.debug("Menu shown")

    def hide(self):
        """Hide the menu panel."""
        if self.initialized and self.panel:
            self.panel.hide()
            self.visible = False
            self.logger.debug("Menu hidden")

    def draw(self, screen):
        """
        Draw the complete menu with background, border, title, and items.
        
        Args:
            screen: Pygame surface to draw on
        """
        self.screen = screen
        
        # Initialize if not already done
        if not self.initialized:
            self.initialize(screen)
        
        # Show the menu panel
        self.show()
        
        # Create a semi-transparent layer over the whole screen
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # Semi-transparent black overlay
        screen.blit(overlay, (0, 0))
        
        # Draw the UI elements
        self.ui_manager.draw_ui(screen)

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
        if not self.initialized or not self.visible:
            return None
            
        # Process the event with pygame_gui
        self.ui_manager.process_events(event)
        
        # Handle keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move selection up
                new_index = (self.selected_index - 1) % len(self.items)
                self.set_selected(new_index)
                return None
                
            elif event.key == pygame.K_DOWN:
                # Move selection down
                new_index = (self.selected_index + 1) % len(self.items)
                self.set_selected(new_index)
                return None
                
            elif event.key == pygame.K_RETURN:
                # Activate selected item
                if self.items[self.selected_index].enabled and self.items[self.selected_index].action:
                    # Store the action result
                    result = self.items[self.selected_index].action()
                    
                    # Hide the menu after action is executed
                    self.hide()
                    
                    # Return the action result
                    return result
        
        # Handle button clicks
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Find which button was pressed
                for i, button in enumerate(self.buttons):
                    if event.ui_element == button:
                        # Update selected index
                        self.selected_index = i
                        
                        # Call the action if enabled
                        if self.items[i].enabled and self.items[i].action:
                            # Store the action result
                            result = self.items[i].action()
                            
                            # Hide the menu after action is executed
                            self.hide()
                            
                            # Return the action result
                            return result
        
        return None
    
    def update(self, time_delta):
        """
        Update the menu UI elements.
        
        Args:
            time_delta (float): Time passed since last update in seconds
        """
        if self.initialized:
            self.ui_manager.update(time_delta)
