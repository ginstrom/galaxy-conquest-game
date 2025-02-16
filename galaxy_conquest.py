"""
Galaxy Conquest - A space exploration game.

This is the main game module that handles the core game loop, state management,
and high-level game mechanics. It implements the main Game class which manages:
- Game initialization and resource loading
- State transitions between menus and gameplay views
- Save/load functionality
- User input handling
- Rendering of game views
"""

import json
import logging
import pygame
import random

from game.debug import debug, clear_debug, draw_debug, toggle_debug, is_debug_enabled
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, NUM_STAR_SYSTEMS,
    WHITE, GRAY
)
from game.enums import GameState, StarType
from game.menu import Menu, MenuItem
from game.star_system import StarSystem
from game.background import BackgroundEffect
from game.resources import ResourceManager
from game.views import GalaxyView, SystemView, PlanetView
from game.views.startup import StartupView
from game.transitions import ViewTransition, ViewStateManager
from game.persistence import save_game_state, load_game_state, save_exists

logger = logging.getLogger(__name__)


class Game:
    """
    Main game class that manages the game state, resources, and rendering.
    
    This class is responsible for:
    - Initializing Pygame and loading game resources
    - Managing game state transitions
    - Handling user input
    - Rendering different game views (galaxy, system, menus)
    - Save/load game functionality
    """
    
    def __init__(self):
        pygame.init()

        self.resource_manager = ResourceManager()
        
        # Initialize view transition system
        self.transition = ViewTransition()
        self.view_state = ViewStateManager()
        
        # Create window without OpenGL
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Galaxy Conquest")
        self.clock = pygame.time.Clock()
        
        # Load planet images
        self.planet_images = {
            'desert': self.resource_manager.load_image('desert_planet', 'img/planet1.png').convert_alpha(),
            'oceanic': self.resource_manager.load_image('oceanic_planet', 'img/planet2.png').convert_alpha()
        }
        
        # Initialize fonts
        self.title_font = self.resource_manager.get_font(48)
        self.info_font = self.resource_manager.get_font(36)
        self.detail_font = self.resource_manager.get_font(24)
        
        # Info panel settings
        self.info_panel_width = 300
        self.info_panel_rect = pygame.Rect(
            SCREEN_WIDTH - self.info_panel_width, 0,
            self.info_panel_width, SCREEN_HEIGHT
        )
        
        # Initialize views
        self.startup_view = StartupView(self)
        self.galaxy_view = GalaxyView(self)
        self.system_view = SystemView(self)
        self.planet_view = PlanetView(self)
        
        # Save notification
        self.save_notification_time = 0
        self.save_notification_duration = 2000  # 2 seconds
        
        # Initialize game state
        self.state = GameState.STARTUP_MENU
        self.selected_system = None
        self.selected_planet = None
        self.hovered_system = None
        self.star_systems = []
        self.background = BackgroundEffect()
        
        # Initialize menus
        self.create_menus()
    
    def create_menus(self):
        # In-game menu (when pressing ESC from galaxy view)
        galaxy_menu_items = [
            MenuItem("New Game", self.new_game),
            MenuItem("Save", self.save_game),
            MenuItem("Resume Game", self.return_to_game),
            MenuItem("Main Menu", self.quit_to_main_menu),
            MenuItem("Quit to Desktop", self.quit_game)
        ]
        self.galaxy_menu = Menu(galaxy_menu_items, "Pause")

        # In-game menu (when pressing ESC from system view)
        system_menu_items = [
            MenuItem("Resume Game", self.return_to_game),
            MenuItem("Galaxy View", self.go_to_galaxy_view),
            MenuItem("Quit to Desktop", self.quit_game)
        ]
        self.system_menu = Menu(system_menu_items, "Pause")
    
    def new_game(self):
        self.star_systems = []
        self.generate_star_systems()
        self.state = GameState.GALAXY
        return True

    def go_to_galaxy_view(self):
        self.state = GameState.GALAXY
        return True
    
    def generate_star_systems(self):
        """
        Generate star systems with random positions while avoiding overlaps.
        
        Uses a simple collision detection system to ensure star systems don't
        overlap. Will make up to 1000 attempts to place each system.
        """
        attempts = 0
        max_attempts = 1000  # Maximum attempts to place a system before giving up
        margin = 100  # Minimum distance from screen edges
        
        # Available space for galaxy (accounting for info panel)
        available_width = self.galaxy_view.galaxy_rect.width - margin * 2
        available_height = self.galaxy_view.galaxy_rect.height - margin * 2
        
        while len(self.star_systems) < NUM_STAR_SYSTEMS and attempts < max_attempts:
            # Generate positions within the available space
            x = random.randint(margin, available_width)
            y = random.randint(margin, available_height)
            
            new_system = StarSystem(x, y, self)
            
            collision = False
            for existing_system in self.star_systems:
                if new_system.collides_with(existing_system):
                    collision = True
                    break
            
            if not collision:
                self.star_systems.append(new_system)
            
            attempts += 1
    
    def save_game(self):
        """
        Save the current game state.
        
        Returns:
            bool: True if called from menu (to return to game), False otherwise
        """
        save_game_state(self.star_systems, self.selected_system)
        
        # Set notification time when game is saved
        self.save_notification_time = pygame.time.get_ticks()
        
        # If called from menu, return to game
        if self.state == GameState.GALAXY_MENU:
            self.state = GameState.SYSTEM if self.selected_system else GameState.GALAXY
            return True
        return False

    def load_game(self):
        """
        Load a saved game state.
        
        Returns:
            bool: True if load successful, False if file not found or invalid
        """
        try:
            save_data = load_game_state()
            
            # Store selected system name if one is selected
            selected_system_name = self.selected_system.name if self.selected_system else None
            
            self.star_systems = []
            for system_data in save_data['star_systems']:
                system = StarSystem(
                    system_data['x'], 
                    system_data['y'],
                    self,
                    name=system_data['name'],
                    star_type=system_data['star_type']
                )
                system.size = system_data['size']
                system.color = tuple(system_data['color']) if 'color' in system_data else system.color
                system.planets = system_data['planets']
                
                # Update selected system reference if this is the one that was selected
                if selected_system_name and system.name == selected_system_name:
                    self.selected_system = system
                
                self.star_systems.append(system)
            
            self.state = GameState.GALAXY
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading save file: {e}")
            return False
    
    def continue_game(self):
        return self.load_game()
    
    def return_to_game(self):
        self.state = GameState.SYSTEM if self.selected_system else GameState.GALAXY
        return True
    
    def quit_to_main_menu(self):
        # Start transition effect
        self.transition.start(
            self.state.value,
            GameState.STARTUP_MENU.value
        )
        
        # Store current view state
        self.view_state.store_state(self.state.value, {
            'selected_system': self.selected_system,
            'selected_planet': self.selected_planet
        })
        
        self.state = GameState.STARTUP_MENU
        self.selected_system = None
        self.selected_planet = None
        return True
    
    def quit_game(self):
        return False
    
    def cleanup(self):
        self.resource_manager.cleanup()
        pygame.quit()

    def run(self):
        running = True
        try:
            menu_states = [GameState.STARTUP_MENU, GameState.GALAXY_MENU, GameState.SYSTEM_MENU]
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F5 and self.state not in menu_states:
                            self.save_game()  # Don't use the return value for F5 quick save
                        elif event.key == pygame.K_ESCAPE:
                            if self.state == GameState.SYSTEM:
                                self.state = GameState.SYSTEM_MENU
                            elif self.state == GameState.GALAXY:
                                self.state = GameState.GALAXY_MENU
                        elif event.key == pygame.K_F4:  
                            toggle_debug()
                    
                    # Handle menu input first
                    if self.state == GameState.STARTUP_MENU:
                        result = self.startup_view.handle_input(event)
                        if result is not None:
                            running = result
                    elif self.state == GameState.SYSTEM_MENU:
                        result = self.system_menu.handle_input(event)
                        if result is not None:
                            running = result
                    elif self.state == GameState.GALAXY_MENU:
                        result = self.galaxy_menu.handle_input(event)
                        if result is not None:
                            running = result
                    # Handle game input only if not in menu
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.state == GameState.GALAXY:
                            self.galaxy_view.handle_click(event.pos)
                        elif self.state == GameState.SYSTEM:
                            self.system_view.handle_click(event.pos)
                
                # Clear debug info at start of frame
                clear_debug()
                
                # Update hovered system in galaxy view
                self.hovered_system = None  # Clear hover state by default
                if self.state == GameState.GALAXY:
                    mouse_pos = pygame.mouse.get_pos()
                    # Only check for hover if mouse is in galaxy area
                    if self.galaxy_view.galaxy_rect.collidepoint(mouse_pos):
                        for system in self.star_systems:
                            if system.rect.collidepoint(mouse_pos):
                                self.hovered_system = system
                                debug(f"Hovering: {system.name} at {system.x}, {system.y}")
                                debug(f"Mouse pos: {mouse_pos}")
                                debug(f"System rect: {system.rect}")
                                break
                
                # Draw
                self.screen.fill((0, 0, 0))
                
                if self.state == GameState.STARTUP_MENU:
                    self.startup_view.draw(self.screen)
                elif self.state == GameState.GALAXY:
                    self.galaxy_view.draw(self.screen)
                    if is_debug_enabled():
                        debug(f"Systems: {len(self.star_systems)}")
                        debug(f"Mouse: {pygame.mouse.get_pos()}")
                elif self.state == GameState.SYSTEM:
                    self.system_view.draw(self.screen)
                    if is_debug_enabled() and self.selected_system:
                        debug(f"System: {self.selected_system.name}")
                        debug(f"Planets: {len(self.selected_system.planets)}")
                        debug(f"Mouse: {pygame.mouse.get_pos()}")
                        if self.selected_planet:
                            debug(f"Selected: {self.selected_planet['name']}")
                elif self.state == GameState.GALAXY_MENU:
                    self.galaxy_view.draw(self.screen)  # Draw game as background
                    self.galaxy_menu.draw(self.screen)
                elif self.state == GameState.SYSTEM_MENU:
                    if self.selected_system:
                        self.system_view.draw(self.screen)  # Draw game as background
                    elif self.selected_planet:
                        self.planet_view.draw(self.screen)
                    self.system_menu.draw(self.screen)
                
                # Draw save notification
                self.draw_save_notification(self.screen)
                
                # Draw active transition effect if any
                if self.transition.is_active:
                    self.transition.draw(self.screen)
                
                # Draw debug last
                draw_debug(self.screen)
                
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            logger.error(f"Error in game loop: {e}")
            raise
        finally:
            self.cleanup() 

    def draw_info_panel(self, screen):
        """
        Draw the information panel on the right side of the screen.
        
        Displays different information based on the current game state:
        - Galaxy view: Shows hovered system info or general galaxy stats
        - System view: Shows selected system info and selected planet details
        
        Args:
            screen: The pygame surface to draw on
        """
        # Draw panel background
        pygame.draw.rect(screen, (30, 30, 30), self.info_panel_rect)
        pygame.draw.line(screen, WHITE, 
                        (self.info_panel_rect.left, 0),
                        (self.info_panel_rect.left, SCREEN_HEIGHT))
        
        # Draw system info
        if self.state == GameState.GALAXY:
            if self.hovered_system:
                # Show hover info in galaxy view
                y = 20
                name_text = self.title_font.render(self.hovered_system.name, True, WHITE)
                screen.blit(name_text, (self.info_panel_rect.left + 10, y))
                
                y += 50
                type_text = self.info_font.render(
                    f"Type: {self.hovered_system.star_type.value}",
                    True, self.hovered_system.color
                )
                screen.blit(type_text, (self.info_panel_rect.left + 10, y))
                
                y += 40
                planets_text = self.info_font.render(
                    f"Planets: {len(self.hovered_system.planets)}",
                    True, WHITE
                )
                screen.blit(planets_text, (self.info_panel_rect.left + 10, y))
            else:
                # Show default galaxy view info
                y = 20
                title_text = self.title_font.render("Galaxy View", True, WHITE)
                screen.blit(title_text, (self.info_panel_rect.left + 10, y))
                
                y += 50
                info_text = self.info_font.render(
                    f"Systems: {len(self.star_systems)}",
                    True, WHITE
                )
                screen.blit(info_text, (self.info_panel_rect.left + 10, y))
                
                y += 40
                help_text = self.detail_font.render(
                    "Hover over a star system",
                    True, WHITE
                )
                screen.blit(help_text, (self.info_panel_rect.left + 10, y))
                
                y += 25
                help_text2 = self.detail_font.render(
                    "for more information",
                    True, WHITE
                )
                screen.blit(help_text2, (self.info_panel_rect.left + 10, y))
        elif self.selected_system:
            # Existing selected system info display
            y = 20
            name_text = self.title_font.render(self.selected_system.name, True, WHITE)
            screen.blit(name_text, (self.info_panel_rect.left + 10, y))
            
            y += 50
            type_text = self.info_font.render(
                f"Type: {self.selected_system.star_type.value}",
                True, self.selected_system.color
            )
            screen.blit(type_text, (self.info_panel_rect.left + 10, y))
            
            y += 40
            planets_text = self.info_font.render(
                f"Planets: {len(self.selected_system.planets)}",
                True, WHITE
            )
            screen.blit(planets_text, (self.info_panel_rect.left + 10, y))
            
            # Draw selected planet info
            if self.selected_planet and self.state == GameState.SYSTEM:
                y += 60
                pygame.draw.line(screen, GRAY,
                            (self.info_panel_rect.left + 10, y),
                            (self.info_panel_rect.right - 10, y))
                
                y += 20
                planet_name = self.info_font.render(
                    self.selected_planet['name'],
                    True, WHITE
                )
                screen.blit(planet_name, (self.info_panel_rect.left + 10, y))
                
                y += 40
                planet_type = self.info_font.render(
                    f"Type: {self.selected_planet['type'].value}",
                    True, WHITE
                )
                screen.blit(planet_type, (self.info_panel_rect.left + 10, y))
                
                y += 40
                resources_title = self.info_font.render("Resources:", True, WHITE)
                screen.blit(resources_title, (self.info_panel_rect.left + 10, y))
                
                y += 30
                for resource in self.selected_planet['resources']:
                    resource_text = self.detail_font.render(
                        f"{resource['type'].value}: {resource['amount']}",
                        True, WHITE
                    )
                    screen.blit(resource_text, (self.info_panel_rect.left + 20, y))
                    y += 25

    def draw_save_notification(self, screen):
        """
        Draw a temporary notification when the game is saved.
        
        Shows a fading "Game Saved!" message in the center top of the screen.
        The notification fades out over 2 seconds.
        
        Args:
            screen: The pygame surface to draw on
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.save_notification_time < self.save_notification_duration:
            # Calculate alpha based on time remaining
            alpha = 255 * (1 - (current_time - self.save_notification_time) / self.save_notification_duration)
            
            # Create text surface
            notification_text = self.info_font.render("Game Saved!", True, WHITE)
            text_rect = notification_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            
            # Create surface with transparency
            text_surface = pygame.Surface(notification_text.get_size(), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, int(alpha)))
            notification_text.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Draw to screen
            screen.blit(notification_text, text_rect)

if __name__ == '__main__':
    game = Game()
    game.run()
