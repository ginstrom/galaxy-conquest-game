"""Galaxy Conquest - A space exploration game."""

from datetime import datetime
from debug import debug, clear_debug, draw_debug, toggle_debug, is_debug_enabled
import json
import logging
import math
import os
import pygame
import random

from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, NUM_STAR_SYSTEMS,
    WHITE, GRAY
)
from game.enums import GameState, StarType, PlanetType, ResourceType
from game.menu import Menu, MenuItem
from game.star_system import StarSystem
from game.background import BackgroundEffect
from game.resources import ResourceManager

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()

        self.resource_manager = ResourceManager()
        
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
        
        # Galaxy view settings
        self.galaxy_rect = pygame.Rect(
            0, 0,
            SCREEN_WIDTH - self.info_panel_width, SCREEN_HEIGHT
        )
        
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
        # Startup menu
        startup_menu_items = [
            MenuItem("New Game", self.new_game),
            MenuItem("Continue", self.continue_game, os.path.exists("saves/autosave.json")),
            MenuItem("Quit", self.quit_game)
        ]
        self.startup_menu = Menu(startup_menu_items, "Galaxy Conquest")
        
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
        attempts = 0
        max_attempts = 1000
        margin = 100
        
        # Available space for galaxy (accounting for info panel)
        available_width = self.galaxy_rect.width - margin * 2
        available_height = self.galaxy_rect.height - margin * 2
        
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
        # Convert planet data to JSON-serializable format
        def convert_planet_data(planet):
            planet_copy = planet.copy()
            planet_copy['type'] = planet['type'].name  # Convert PlanetType enum
            
            # Convert resources data
            resources_copy = []
            for resource in planet['resources']:
                resource_copy = resource.copy()
                resource_copy['type'] = resource['type'].name  # Convert ResourceType enum
                resources_copy.append(resource_copy)
            planet_copy['resources'] = resources_copy
            
            # Ensure angle and orbit_speed are included
            if 'angle' not in planet_copy:
                planet_copy['angle'] = random.uniform(0, 2 * math.pi)
            if 'orbit_speed' not in planet_copy:
                planet_copy['orbit_speed'] = random.uniform(0.2, 0.5)
            
            return planet_copy

        save_data = {
            'star_systems': [
                {
                    'x': system.x,
                    'y': system.y,
                    'name': system.name,
                    'star_type': system.star_type.name,
                    'size': system.size,
                    'color': system.color,
                    'planets': [convert_planet_data(p) for p in system.planets]
                }
                for system in self.star_systems
            ],
            'selected_system': self.selected_system.name if self.selected_system else None,
            'timestamp': datetime.now().isoformat()
        }
        
        os.makedirs('saves', exist_ok=True)
        with open('saves/autosave.json', 'w') as f:
            json.dump(save_data, f, indent=2)
        
        # Set notification time when game is saved
        self.save_notification_time = pygame.time.get_ticks()
        
        # If called from menu, return to game
        if self.state == GameState.GALAXY_MENU:
            self.state = GameState.SYSTEM if self.selected_system else GameState.GALAXY
            return True
        return False

    def load_game(self):
        try:
            with open('saves/autosave.json', 'r') as f:
                save_data = json.load(f)
            
            # Store selected system name if one is selected
            selected_system_name = self.selected_system.name if self.selected_system else None
            
            self.star_systems = []
            for system_data in save_data['star_systems']:
                system = StarSystem(
                    system_data['x'], 
                    system_data['y'],
                    self,
                    name=system_data['name'],
                    star_type=StarType[system_data['star_type']]
                )
                system.size = system_data['size']
                
                # Restore color if it exists in save data, otherwise use the generated color
                if 'color' in system_data:
                    system.color = tuple(system_data['color'])
                
                # Convert planet type strings back to enums
                planets = []
                for planet in system_data['planets']:
                    planet_copy = planet.copy()
                    planet_copy['type'] = PlanetType[planet['type']]
                    
                    # Convert resource type strings back to enums
                    resources = []
                    for resource in planet['resources']:
                        resource_copy = resource.copy()
                        resource_copy['type'] = ResourceType[resource['type']]
                        resources.append(resource_copy)
                    planet_copy['resources'] = resources
                    planets.append(planet_copy)
                system.planets = planets
                
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
                    if self.state in menu_states:
                        if self.state == GameState.SYSTEM_MENU:
                            menu = self.system_menu
                        elif self.state == GameState.GALAXY_MENU:
                            menu = self.galaxy_menu
                        else:
                            menu = self.startup_menu
                        result = menu.handle_input(event)
                        if result is not None:
                            running = result
                    # Handle game input only if not in menu
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.state == GameState.GALAXY:
                            self.handle_galaxy_click(event.pos)
                        elif self.state == GameState.SYSTEM:
                            self.handle_system_click(event.pos)
                
                # Clear debug info at start of frame
                clear_debug()
                
                # Update hovered system in galaxy view
                self.hovered_system = None  # Clear hover state by default
                if self.state == GameState.GALAXY:
                    mouse_pos = pygame.mouse.get_pos()
                    # Only check for hover if mouse is in galaxy area
                    if self.galaxy_rect.collidepoint(mouse_pos):
                        for system in self.star_systems:
                            if system.rect.collidepoint(mouse_pos):
                                self.hovered_system = system
                                debug(f"Hovering: {system.name} at {system.x}, {system.y}")
                                debug(f"Mouse pos: {mouse_pos}")
                                debug(f"System rect: {system.rect}")
                                break
                
                # Draw
                self.screen.fill((0, 0, 0))
                
                if self.state == GameState.GALAXY:
                    self.draw_galaxy_view()
                    if is_debug_enabled():
                        debug(f"Systems: {len(self.star_systems)}")
                        debug(f"Mouse: {pygame.mouse.get_pos()}")
                elif self.state == GameState.SYSTEM:
                    self.draw_system_view()
                    if is_debug_enabled() and self.selected_system:
                        debug(f"System: {self.selected_system.name}")
                        debug(f"Planets: {len(self.selected_system.planets)}")
                        debug(f"Mouse: {pygame.mouse.get_pos()}")
                        if self.selected_planet:
                            debug(f"Selected: {self.selected_planet['name']}")
                elif self.state == GameState.STARTUP_MENU:
                    self.draw_galaxy_view()  # Draw game as background
                    self.startup_menu.draw(self.screen)
                elif self.state == GameState.GALAXY_MENU:
                    self.draw_galaxy_view()  # Draw game as background
                    self.galaxy_menu.draw(self.screen)
                elif self.state == GameState.SYSTEM_MENU:
                    if self.selected_system:
                        self.draw_system_view()  # Draw game as background
                    elif self.selected_planet:
                        self.draw_planet_view()
                    self.system_menu.draw(self.screen)
                
                # Draw save notification on top
                self.draw_save_notification(self.screen)
                
                # Draw debug last
                draw_debug(self.screen)
                
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            logger.error(f"Error in game loop: {e}")
            raise
        finally:
            self.cleanup() 

    def handle_galaxy_click(self, pos):
        """Handle mouse click in galaxy view."""
        # Only handle clicks in the galaxy area
        if not self.galaxy_rect.collidepoint(pos):
            return
            
        for system in self.star_systems:
            if system.rect.collidepoint(pos):
                self.selected_system = system
                debug(f"Selected system: {system.name}")
                debug(f"Click pos: {pos}")
                debug(f"System rect: {system.rect}")
                self.state = GameState.SYSTEM
                break

    def handle_system_click(self, pos):
        """Handle mouse click in system view."""
        if not self.selected_system:
            return
        
        # Adjust click position to account for info panel
        panel_width = 300  # Match the info panel width
        available_width = SCREEN_WIDTH - panel_width
        center_x = available_width // 2
        center_y = SCREEN_HEIGHT // 2
        
        for planet in self.selected_system.planets:
            x = planet['x']
            y = planet['y']
            
            # Check if click is within planet's radius
            dx = pos[0] - x
            dy = pos[1] - y
            if dx * dx + dy * dy <= planet['size'] * planet['size']:
                self.selected_planet = planet
                self.state = GameState.SYSTEM  # Ensure we're in SYSTEM state when planet is selected
                break

    def draw_galaxy_view(self):
        """Draw the galaxy view."""
        # Draw background
        self.background.draw_galaxy_background(self.screen)
        
        # Draw star systems
        for system in self.star_systems:
            system.draw_galaxy_view(self.screen)
        
        # Draw info panel
        self.draw_info_panel(self.screen)
        
        # Draw vertical line to separate info panel
        pygame.draw.line(
            self.screen, 
            WHITE,
            (self.galaxy_rect.right, 0),
            (self.galaxy_rect.right, SCREEN_HEIGHT)
        )

    def draw_system_view(self):
        """Draw the system view."""
        # Draw background
        self.background.draw_system_background(self.screen)
        
        if self.selected_system:
            # Draw the system
            self.selected_system.draw_system_view(self.screen)
            
            # Draw info panel
            self.draw_info_panel(self.screen)

    def draw_info_panel(self, screen):
        """Draw the information panel."""
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
        """Draw the save notification if active."""
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
