"""
Information panel view module.

This module contains the InfoPanel base class and its subclasses that handle rendering
the information panel displaying game state information such as:
- Galaxy view: Shows hovered system info or general galaxy stats
- System view: Shows selected system info and selected planet details
- Planet view: Shows detailed planet information
"""

import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UILabel
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GRAY
from game.enums import GameState
from game.logging_config import get_logger


class InfoPanel:
    """
    Base view class for rendering the information panel.
    
    This class provides common functionality for all info panel views.
    Specific drawing logic is implemented in subclasses for each game state.
    """
    
    def __init__(self, game):
        """
        Initialize the InfoPanel view.
        
        Args:
            game: The main Game instance
        """
        self.logger = get_logger(__name__)
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.game = game
        self.panel_width = 300
        self.panel_rect = pygame.Rect(
            SCREEN_WIDTH - self.panel_width, 0,
            self.panel_width, SCREEN_HEIGHT
        )
        
        # Create the panel using pygame_gui
        self.ui_panel = UIPanel(
            relative_rect=self.panel_rect,
            manager=self.game.ui_manager
        )
        
        # List to keep track of UI elements
        self.ui_elements = []
    
    def draw(self, screen):
        """
        Draw the information panel.
        
        Base implementation does nothing as pygame_gui handles the drawing.
        Subclasses should override this method to update UI elements based on game state.
        
        Args:
            screen: The pygame surface to draw on
        """
        # The actual drawing is handled by pygame_gui
        pass
    
    def clear_ui_elements(self):
        """
        Remove all UI elements from the panel.
        """
        for element in self.ui_elements:
            element.kill()
        self.ui_elements = []
    
    def create_label(self, text, rect, font_size=None, text_color=None, is_title=False):
        """
        Create a UILabel and add it to the panel.
        
        Args:
            text: The text to display
            rect: The pygame.Rect for positioning the label
            font_size: Optional font size (default: None, uses pygame_gui default)
            text_color: Optional text color (default: None, uses pygame_gui default)
            is_title: Whether this is a title label (affects styling)
            
        Returns:
            The created UILabel
        """
        object_id = "#title_label" if is_title else None
        label = UILabel(
            relative_rect=rect,
            text=text,
            manager=self.game.ui_manager,
            container=self.ui_panel,
            object_id=object_id
        )
        self.ui_elements.append(label)
        return label
    
    def create_horizontal_rule(self, y_position, padding=10):
        """
        Create a horizontal rule (separator line) in the panel.
        
        Args:
            y_position: The y-coordinate for the line
            padding: Padding from the edges (default: 10)
            
        Returns:
            The pygame.Rect object representing the rule
        """
        rule_rect = pygame.Rect(
            padding, 
            y_position, 
            self.panel_width - (padding * 2), 
            2
        )
        
        # Create a panel with the same dimensions as the rule
        # and use it as a separator
        panel = UIPanel(
            relative_rect=rule_rect,
            manager=self.game.ui_manager,
            container=self.ui_panel
        )
        
        self.ui_elements.append(panel)
        return panel
    
    def create_planet_details(self, planet, start_y):
        """
        Create UI elements for displaying planet details.
        
        Args:
            planet: The planet data dictionary
            start_y: The starting y-coordinate for the elements
            
        Returns:
            The updated y-coordinate after creating all elements
        """
        y = start_y
        padding = 10
        
        # Planet name (title)
        name_rect = pygame.Rect(padding, y, self.panel_width - (padding * 2), 40)
        self.create_label(planet['name'], name_rect, is_title=True)
        y += 40
        
        # Planet type
        type_rect = pygame.Rect(padding, y, self.panel_width - (padding * 2), 30)
        self.create_label(f"Type: {planet['type'].value}", type_rect)
        y += 40
        
        # Resources title
        resources_rect = pygame.Rect(padding, y, self.panel_width - (padding * 2), 30)
        self.create_label("Resources:", resources_rect)
        y += 30
        
        # Resource items
        resources = planet['resources']
        
        # Handle both old list format and new dict format
        if isinstance(resources, list):
            # Old format: list of dicts with 'type' and 'amount' keys
            for resource in resources:
                resource_rect = pygame.Rect(padding + 10, y, self.panel_width - (padding * 2) - 10, 25)
                self.create_label(f"{resource['type'].value}: {resource['amount']}", resource_rect)
                y += 25
        else:
            # New format: dict with resource types as keys and amounts as values
            for resource_type, amount in resources.items():
                resource_rect = pygame.Rect(padding + 10, y, self.panel_width - (padding * 2) - 10, 25)
                self.create_label(f"{resource_type.value}: {amount}", resource_rect)
                y += 25
        
        return y
    
    def handle_input(self, event):
        """Handle input events (no-op implementation)."""
        pass
    
    def handle_click(self, pos):
        """Handle mouse click events (no-op implementation)."""
        pass
    
    def handle_keydown(self, event):
        """Handle keydown events (no-op implementation)."""
        pass


class GalaxyViewInfoPanel(InfoPanel):
    """
    InfoPanel subclass for the galaxy view.
    
    Responsible for displaying:
    - Hovered system information
    - General galaxy statistics when no system is hovered
    """
    
    def __init__(self, game):
        """
        Initialize the GalaxyViewInfoPanel.
        
        Args:
            game: The main Game instance
        """
        super().__init__(game)
        self.last_hovered_system = None
    
    def draw(self, screen):
        """
        Update the galaxy view information panel.
        
        This method checks if the hovered system has changed and updates
        the UI elements accordingly.
        
        Args:
            screen: The pygame surface to draw on (not used directly)
        """
        # Call the parent draw method (which does nothing but is kept for consistency)
        super().draw(screen)
        
        # Check if we need to update the UI elements
        if self.game.hovered_system != self.last_hovered_system:
            self.clear_ui_elements()
            
            if self.game.hovered_system:
                # Show hover info in galaxy view
                self._create_system_info(self.game.hovered_system)
            else:
                # Show default galaxy view info
                self._create_default_info()
            
            self.last_hovered_system = self.game.hovered_system
    
    def _create_system_info(self, system):
        """
        Create UI elements for displaying system information.
        
        Args:
            system: The star system to display information for
        """
        padding = 10
        
        # System name (title)
        name_rect = pygame.Rect(padding, 20, self.panel_width - (padding * 2), 40)
        self.create_label(system.name, name_rect, is_title=True)
        
        # System type
        type_rect = pygame.Rect(padding, 70, self.panel_width - (padding * 2), 30)
        self.create_label(f"Type: {system.star_type.value}", type_rect)
        
        # Planet count
        planets_rect = pygame.Rect(padding, 110, self.panel_width - (padding * 2), 30)
        self.create_label(f"Planets: {len(system.planets)}", planets_rect)
    
    def _create_default_info(self):
        """
        Create UI elements for displaying default galaxy view information.
        """
        padding = 10
        
        # Title
        title_rect = pygame.Rect(padding, 20, self.panel_width - (padding * 2), 40)
        self.create_label("Galaxy View", title_rect, is_title=True)
        
        # System count
        systems_rect = pygame.Rect(padding, 70, self.panel_width - (padding * 2), 30)
        self.create_label(f"Systems: {len(self.game.star_systems)}", systems_rect)
        
        # Help text
        help_rect1 = pygame.Rect(padding, 110, self.panel_width - (padding * 2), 25)
        self.create_label("Hover over a star system", help_rect1)
        
        help_rect2 = pygame.Rect(padding, 135, self.panel_width - (padding * 2), 25)
        self.create_label("for more information", help_rect2)


class SystemViewInfoPanel(InfoPanel):
    """
    InfoPanel subclass for the system view.
    
    Responsible for displaying:
    - Selected system information
    - Selected planet details
    - Hovered planet details
    """
    
    def __init__(self, game):
        """
        Initialize the SystemViewInfoPanel.
        
        Args:
            game: The main Game instance
        """
        super().__init__(game)
        self.last_hovered_planet = None
        self.last_selected_planet = None
        self.last_selected_system = None
    
    def draw(self, screen):
        """
        Update the system view information panel.
        
        This method checks if the selected system, selected planet, or hovered planet
        has changed and updates the UI elements accordingly.
        
        Args:
            screen: The pygame surface to draw on (not used directly)
        """
        # Call the parent draw method (which does nothing but is kept for consistency)
        super().draw(screen)
        
        # Check if we need to update the UI elements
        if (self.game.selected_system != self.last_selected_system or
            self.game.selected_planet != self.last_selected_planet or
            self.game.hovered_planet != self.last_hovered_planet):
            
            self.clear_ui_elements()
            
            if self.game.selected_system:
                # Create system info elements
                y = self._create_system_info(self.game.selected_system)
                
                # Draw hovered planet info if available
                if self.game.hovered_planet and self.game.state == GameState.SYSTEM:
                    self.create_horizontal_rule(y)
                    self.create_planet_details(self.game.hovered_planet, y + 20)
                
                # Draw selected planet info if no planet is hovered
                elif self.game.selected_planet and self.game.state == GameState.SYSTEM:
                    self.create_horizontal_rule(y)
                    self.create_planet_details(self.game.selected_planet, y + 20)
            
            # Update tracking variables
            self.last_selected_system = self.game.selected_system
            self.last_selected_planet = self.game.selected_planet
            self.last_hovered_planet = self.game.hovered_planet
    
    def _create_system_info(self, system):
        """
        Create UI elements for displaying system information.
        
        Args:
            system: The star system to display information for
            
        Returns:
            The y-coordinate after the last element
        """
        padding = 10
        
        # System name (title)
        name_rect = pygame.Rect(padding, 20, self.panel_width - (padding * 2), 40)
        self.create_label(system.name, name_rect, is_title=True)
        
        # System type
        type_rect = pygame.Rect(padding, 70, self.panel_width - (padding * 2), 30)
        self.create_label(f"Type: {system.star_type.value}", type_rect)
        
        # Planet count
        planets_rect = pygame.Rect(padding, 110, self.panel_width - (padding * 2), 30)
        self.create_label(f"Planets: {len(system.planets)}", planets_rect)
        
        return 170  # Return the y-coordinate after the system info


class PlanetViewInfoPanel(InfoPanel):
    """
    InfoPanel subclass for the planet view.
    
    Responsible for displaying:
    - Detailed planet information
    - Planet resources and properties
    """
    
    def __init__(self, game):
        """
        Initialize the PlanetViewInfoPanel.
        
        Args:
            game: The main Game instance
        """
        super().__init__(game)
        self.last_selected_planet = None
        self.last_selected_system = None
    
    def draw(self, screen):
        """
        Update the planet view information panel.
        
        This method checks if the selected system or selected planet has changed
        and updates the UI elements accordingly.
        
        Args:
            screen: The pygame surface to draw on (not used directly)
        """
        # Call the parent draw method (which does nothing but is kept for consistency)
        super().draw(screen)
        
        # Check if we need to update the UI elements
        if (self.game.selected_system != self.last_selected_system or
            self.game.selected_planet != self.last_selected_planet):
            
            self.clear_ui_elements()
            
            if self.game.selected_planet:
                # Display selected system info if available
                if self.game.selected_system:
                    y = self._create_system_info(self.game.selected_system)
                    self.create_horizontal_rule(y)
                    self.create_planet_details(self.game.selected_planet, y + 20)
                else:
                    self.create_planet_details(self.game.selected_planet, 20)
            
            # Update tracking variables
            self.last_selected_system = self.game.selected_system
            self.last_selected_planet = self.game.selected_planet
    
    def _create_system_info(self, system):
        """
        Create UI elements for displaying system information.
        
        Args:
            system: The star system to display information for
            
        Returns:
            The y-coordinate after the last element
        """
        padding = 10
        
        # System name (title)
        name_rect = pygame.Rect(padding, 20, self.panel_width - (padding * 2), 40)
        self.create_label(system.name, name_rect, is_title=True)
        
        # System type
        type_rect = pygame.Rect(padding, 70, self.panel_width - (padding * 2), 30)
        self.create_label(f"Type: {system.star_type.value}", type_rect)
        
        # Planet count
        planets_rect = pygame.Rect(padding, 110, self.panel_width - (padding * 2), 30)
        self.create_label(f"Planets: {len(system.planets)}", planets_rect)
        
        return 170  # Return the y-coordinate after the system info
