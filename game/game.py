"""
Game module for Galaxy Conquest.

This module contains the main Game class that handles the core game loop, state management,
and high-level game mechanics. It implements the main Game class which manages:
- Game initialization and resource loading
- Save/load functionality
- User input handling
- Rendering of game views
"""

import json
import pygame
import pygame_gui
import random

from game.debug import debug, clear_debug, draw_debug, toggle_debug
from game.views.hover_utils import check_hover, is_within_circle
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, NUM_STAR_SYSTEMS,
    WHITE, GRAY
)
from game.enums import GameState, StarType
from game.menu import Menu, MenuItem
from game.star_system import StarSystem
from game.background import BackgroundEffect
from game.resources import ResourceManager, ResourceManagerFactory
from game.views import GalaxyView, SystemView, PlanetView, InfoPanel
from game.views.startup import StartupView
from game.persistence import save_game_state, load_game_state, save_exists
from game.logging_config import configure_logging, get_logger


class Game:
    """
    Main game class that manages the game state, resources, and rendering.
    
    This class is responsible for:
    - Initializing Pygame and loading game resources
    - Handling user input
    - Rendering different game views (galaxy, system, menus)
    - Save/load game functionality
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing game")
        
        pygame.init()
        self.logger.debug("Pygame initialized")

        self.resource_manager = ResourceManagerFactory.create()
        self.logger.debug("Resource manager created")
        
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
        self.logger.debug("Planet images loaded")
        
        # Initialize fonts
        self.title_font = self.resource_manager.get_font(48)
        self.info_font = self.resource_manager.get_font(36)
        self.detail_font = self.resource_manager.get_font(24)
        self.logger.debug("Fonts initialized")
        
        # Initialize pygame_gui
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.logger.debug("UI manager initialized")
        
        # Initialize views
        self.startup_view = StartupView(self)
        self.galaxy_view = GalaxyView(self)
        self.system_view = SystemView(self)
        self.planet_view = PlanetView(self)
        self.logger.debug("Views initialized")
        
        # Save notification
        self.save_notification_time = 0
        self.save_notification_duration = 2000  # 2 seconds
        
        # Initialize game state
        self.state = GameState.STARTUP_MENU
        self.current_view = self.startup_view
        self.selected_system = None
        self.selected_planet = None
        self.hovered_system = None
        self.hovered_planet = None  # Track hovered planet in system view
        self.star_systems = []
        self.background = BackgroundEffect()
        self.logger.debug("Game state initialized")
        
        # Initialize menus
        self.init_menus()
        self.logger.info("Game initialization complete")
    
    def init_menus(self):
        # In-game menu (when pressing ESC from galaxy view)
        self.galaxy_menu = self.galaxy_view.menu
        self.system_menu = self.system_view.menu
        self.logger.debug("Menus initialized")
    
    def new_game(self):
        self.logger.info("Starting new game")
        self.star_systems = []
        self.generate_star_systems()
        self.state = GameState.GALAXY
        self.current_view = self.galaxy_view
        return True

    def go_to_galaxy_view(self):
        self.logger.debug("Switching to galaxy view")
        self.state = GameState.GALAXY
        self.current_view = self.galaxy_view
        return True
    
    def generate_star_systems(self):
        """
        Generate star systems with random positions while avoiding overlaps.
        
        Uses a simple collision detection system to ensure star systems don't
        overlap. Will make up to 1000 attempts to place each system.
        """
        self.logger.info(f"Generating {NUM_STAR_SYSTEMS} star systems")
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
                self.logger.debug(f"Created star system: {new_system.name} at ({x}, {y})")
            
            attempts += 1
        
        self.logger.info(f"Generated {len(self.star_systems)} star systems in {attempts} attempts")
    
    def save_game(self):
        """
        Save the current game state.
        
        Returns:
            bool: True if called from menu (to return to game), False otherwise
        """
        self.logger.info("Saving game state")
        save_game_state(self.star_systems, self.selected_system)
        
        # Set notification time when game is saved
        self.save_notification_time = pygame.time.get_ticks()
        
        # If called from menu, return to game
        if self.state == GameState.GALAXY_MENU:
            if self.selected_system:
                self.state = GameState.SYSTEM
                self.current_view = self.system_view
            else:
                self.state = GameState.GALAXY
                self.current_view = self.galaxy_view
            return True
        return False

    def load_game(self):
        """
        Load a saved game state.
        
        Returns:
            bool: True if load successful, False if file not found or invalid
        """
        self.logger.info("Loading game state")
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
                self.logger.debug(f"Loaded star system: {system.name}")
            
            self.state = GameState.GALAXY
            self.current_view = self.galaxy_view
            self.logger.info("Game state loaded successfully")
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Error loading save file: {e}")
            return False
    
    def continue_game(self):
        return self.load_game()
    
    def return_to_game(self):
        self.logger.debug("Returning to game")
        if self.selected_system:
            self.state = GameState.SYSTEM
            self.current_view = self.system_view
        else:
            self.state = GameState.GALAXY
            self.current_view = self.galaxy_view
        return True
    
    def quit_to_main_menu(self):
        self.logger.info("Quitting to main menu")
        self.state = GameState.STARTUP_MENU
        self.current_view = self.startup_view
        self.selected_system = None
        self.selected_planet = None
        return True
    
    def quit_game(self):
        self.logger.info("Quitting game")
        return False
    
    def cleanup(self):
        self.logger.info("Cleaning up resources")
        self.resource_manager.cleanup()
        pygame.quit()

    def run(self):
        self.logger.info("Starting game loop")
        running = True
        try:
            menu_states = [GameState.STARTUP_MENU, GameState.GALAXY_MENU, GameState.SYSTEM_MENU]
            while running:
                time_delta = self.clock.tick(60) / 1000.0  # Time since last frame in seconds
                
                for event in pygame.event.get():
                    # Process pygame_gui events first
                    self.ui_manager.process_events(event)
                    
                    if event.type == pygame.QUIT:
                        running = False
                    
                    elif event.type == pygame.KEYDOWN:
                        # quick save
                        if event.key == pygame.K_F5 and self.state not in menu_states:
                            self.save_game()  # Don't use the return value for F5 quick save
                        # toggle debug info
                        elif event.key == pygame.K_F4:  
                            toggle_debug()
                        # other key events handled by current view
                        else:
                            self.current_view.handle_keydown(event)
                    
                    # Handle menu input first
                    if self.state in menu_states:
                        result = self.current_view.menu.handle_input(event)
                        if result is not None:
                            running = result
                    # Handle game input only if not in menu

                    # handle left click
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.current_view.handle_click(event.pos)

                    # handle right click
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        self.current_view.handle_right_click(event.pos)
                
                # Update pygame_gui
                self.ui_manager.update(time_delta)
                
                # Clear debug info at start of frame
                clear_debug()
                
                # Update hover state based on current view
                self.hovered_system = None  # Clear hover state by default
                self.hovered_planet = None  # Clear hover state by default
                
                if self.state == GameState.GALAXY:
                    mouse_pos = pygame.mouse.get_pos()
                    # Only check for hover if mouse is in galaxy area
                    rect_check_func = lambda pos: self.galaxy_view.galaxy_rect.collidepoint(pos)
                    self.hovered_system = check_hover(
                        mouse_pos, 
                        self.star_systems, 
                        lambda pos, obj: obj.rect.collidepoint(pos),
                        rect_check_func
                    )
                    
                    # Additional debug info if hovering
                    if self.hovered_system:
                        debug(f"Hovering: {self.hovered_system.name} at {self.hovered_system.x}, {self.hovered_system.y}")
                        debug(f"Mouse pos: {mouse_pos}")
                        debug(f"System rect: {self.hovered_system.rect}")
                
                # Draw
                self.screen.fill((0, 0, 0))
                
                self.current_view.draw(self.screen)
                
                # Draw pygame_gui elements
                self.ui_manager.draw_ui(self.screen)
                
                # Draw save notification
                self.draw_save_notification(self.screen)
                
                # Draw debug last
                draw_debug(self.screen)
                
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            self.logger.error(f"Error in game loop: {e}", exc_info=True)
            raise
        finally:
            self.cleanup() 

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
