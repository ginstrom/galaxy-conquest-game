"""
Information panel view module.

This module contains the InfoPanel base class and its subclasses that handle rendering
the information panel displaying game state information such as:
- Galaxy view: Shows hovered system info or general galaxy stats
- System view: Shows selected system info and selected planet details
- Planet view: Shows detailed planet information
"""

import pygame
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
    
    def draw(self, screen):
        """
        Draw the information panel.
        
        Base implementation draws the panel background and border.
        Subclasses should override this method to add view-specific content.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw panel background
        pygame.draw.rect(screen, (30, 30, 30), self.panel_rect)
        pygame.draw.line(screen, WHITE, 
                        (self.panel_rect.left, 0),
                        (self.panel_rect.left, SCREEN_HEIGHT))
    
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
    
    def draw(self, screen):
        """
        Draw the galaxy view information panel.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw the base panel background and border
        super().draw(screen)
        
        if self.game.hovered_system:
            # Show hover info in galaxy view
            y = 20
            name_text = self.game.title_font.render(
                self.game.hovered_system.name, True, WHITE
            )
            screen.blit(name_text, (self.panel_rect.left + 10, y))
            
            y += 50
            type_text = self.game.info_font.render(
                f"Type: {self.game.hovered_system.star_type.value}",
                True, self.game.hovered_system.color
            )
            screen.blit(type_text, (self.panel_rect.left + 10, y))
            
            y += 40
            planets_text = self.game.info_font.render(
                f"Planets: {len(self.game.hovered_system.planets)}",
                True, WHITE
            )
            screen.blit(planets_text, (self.panel_rect.left + 10, y))
        else:
            # Show default galaxy view info
            y = 20
            title_text = self.game.title_font.render("Galaxy View", True, WHITE)
            screen.blit(title_text, (self.panel_rect.left + 10, y))
            
            y += 50
            info_text = self.game.info_font.render(
                f"Systems: {len(self.game.star_systems)}",
                True, WHITE
            )
            screen.blit(info_text, (self.panel_rect.left + 10, y))
            
            y += 40
            help_text = self.game.detail_font.render(
                "Hover over a star system",
                True, WHITE
            )
            screen.blit(help_text, (self.panel_rect.left + 10, y))
            
            y += 25
            help_text2 = self.game.detail_font.render(
                "for more information",
                True, WHITE
            )
            screen.blit(help_text2, (self.panel_rect.left + 10, y))


class SystemViewInfoPanel(InfoPanel):
    """
    InfoPanel subclass for the system view.
    
    Responsible for displaying:
    - Selected system information
    - Selected planet details
    """
    
    def draw(self, screen):
        """
        Draw the system view information panel.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw the base panel background and border
        super().draw(screen)
        
        if self.game.selected_system:
            # Display selected system info
            y = 20
            name_text = self.game.title_font.render(
                self.game.selected_system.name, True, WHITE
            )
            screen.blit(name_text, (self.panel_rect.left + 10, y))
            
            y += 50
            type_text = self.game.info_font.render(
                f"Type: {self.game.selected_system.star_type.value}",
                True, self.game.selected_system.color
            )
            screen.blit(type_text, (self.panel_rect.left + 10, y))
            
            y += 40
            planets_text = self.game.info_font.render(
                f"Planets: {len(self.game.selected_system.planets)}",
                True, WHITE
            )
            screen.blit(planets_text, (self.panel_rect.left + 10, y))
            
            # Draw selected planet info
            if self.game.selected_planet and self.game.state == GameState.SYSTEM:
                y += 60
                pygame.draw.line(screen, GRAY,
                            (self.panel_rect.left + 10, y),
                            (self.panel_rect.right - 10, y))
                
                y += 20
                planet_name = self.game.info_font.render(
                    self.game.selected_planet['name'],
                    True, WHITE
                )
                screen.blit(planet_name, (self.panel_rect.left + 10, y))
                
                y += 40
                planet_type = self.game.info_font.render(
                    f"Type: {self.game.selected_planet['type'].value}",
                    True, WHITE
                )
                screen.blit(planet_type, (self.panel_rect.left + 10, y))
                
                y += 40
                resources_title = self.game.info_font.render("Resources:", True, WHITE)
                screen.blit(resources_title, (self.panel_rect.left + 10, y))
                
                y += 30
                for resource in self.game.selected_planet['resources']:
                    resource_text = self.game.detail_font.render(
                        f"{resource['type'].value}: {resource['amount']}",
                        True, WHITE
                    )
                    screen.blit(resource_text, (self.panel_rect.left + 20, y))
                    y += 25


class PlanetViewInfoPanel(InfoPanel):
    """
    InfoPanel subclass for the planet view.
    
    Responsible for displaying:
    - Detailed planet information
    - Planet resources and properties
    """
    
    def draw(self, screen):
        """
        Draw the planet view information panel.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw the base panel background and border
        super().draw(screen)
        
        if self.game.selected_planet:
            # Display detailed planet information
            y = 20
            planet_name = self.game.title_font.render(
                self.game.selected_planet['name'],
                True, WHITE
            )
            screen.blit(planet_name, (self.panel_rect.left + 10, y))
            
            y += 50
            planet_type = self.game.info_font.render(
                f"Type: {self.game.selected_planet['type'].value}",
                True, WHITE
            )
            screen.blit(planet_type, (self.panel_rect.left + 10, y))
            
            y += 40
            resources_title = self.game.info_font.render("Resources:", True, WHITE)
            screen.blit(resources_title, (self.panel_rect.left + 10, y))
            
            y += 30
            for resource in self.game.selected_planet['resources']:
                resource_text = self.game.detail_font.render(
                    f"{resource['type'].value}: {resource['amount']}",
                    True, WHITE
                )
                screen.blit(resource_text, (self.panel_rect.left + 20, y))
                y += 25
