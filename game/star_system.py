"""Star system and planet generation for Galaxy Conquest."""

import random
import pygame
import math
from .enums import StarType, PlanetType, ResourceType
from .constants import WHITE, GRAY
from .properties import StarProperties, PlanetProperties, NameGenerator

class StarSystem:
    def __init__(self, x, y, game_instance=None, name=None, star_type=None):
        self.x = x
        self.y = y
        self.name = name if name else NameGenerator.generate_name()
        self.star_type = star_type if star_type else StarProperties.get_random_type()
        props = StarProperties.PROPERTIES[self.star_type]
        self.game_instance = game_instance
        
        self.size = random.randint(props['min_size'], props['max_size'])
        self.color = props['color']
        self.planets = []
        self.num_planets = random.randint(props['min_planets'], props['max_planets'])
        self.generate_planets()
        
        # Font setup for names
        self.font = pygame.font.Font(None, 24)
        self.name_surface = self.font.render(self.name, True, WHITE)
        self.name_rect = self.name_surface.get_rect()
        
        # Calculate the total height including text
        text_height = self.name_rect.height
        
        # Update collision rect to be centered on the star
        self.rect = pygame.Rect(self.x - self.size, 
                              self.y - self.size, 
                              self.size * 2, 
                              self.size * 2)  # Make it square, centered on star
        
        # Text position
        self.name_rect.centerx = self.x
        self.name_rect.top = self.y + self.size + 15

    def collides_with(self, other):
        """Check if this star system collides with another."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx * dx + dy * dy)
        min_distance = (self.size + other.size) * 3  # Increased spacing
        return distance < min_distance

    def generate_planets(self):
        """Generate planets for this star system."""
        orbit_spacing = 60  # Base spacing between orbits
        for i in range(self.num_planets):
            planet_type = PlanetProperties.get_random_type()
            props = PlanetProperties.PROPERTIES[planet_type]
            
            size = random.randint(props['min_size'], props['max_size'])
            orbit_number = i + 1
            
            planet = {
                'type': planet_type,
                'size': size,
                'orbit_number': orbit_number,
                'angle': random.uniform(0, 2 * math.pi),
                'orbit_speed': random.uniform(0.2, 0.5),
                'resources': PlanetProperties.generate_resources(planet_type),
                'name': f"{self.name} {orbit_number}"
            }
            self.planets.append(planet)

    def draw_galaxy_view(self, screen):
        """Draw the star system in galaxy view."""
        # Draw the star
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        
        # Draw the name below the star
        screen.blit(self.name_surface, self.name_rect)

    def draw_system_view(self, screen):
        """Draw the star system in system view."""
        # Adjust center position to account for info panel
        panel_width = 300  # Match the info panel width
        available_width = screen.get_width() - panel_width
        center_x = available_width // 2
        center_y = screen.get_height() // 2
        
        # Draw system name at the top
        large_font = pygame.font.Font(None, 48)
        
        # Draw shadow for system name first
        shadow_text = large_font.render(self.name, True, GRAY)
        shadow_rect = shadow_text.get_rect(center=(center_x + 1, center_y//2 + 1))
        screen.blit(shadow_text, shadow_rect)
        
        # Draw main text
        title_text = large_font.render(self.name, True, WHITE)
        title_rect = title_text.get_rect(center=(center_x, center_y//2))
        screen.blit(title_text, title_rect)
        
        # Draw star type below the name
        type_font = pygame.font.Font(None, 36)
        type_text = type_font.render(self.star_type.value, True, self.color)
        type_rect = type_text.get_rect(center=(center_x, center_y//2 + 40))
        screen.blit(type_text, type_rect)
        
        # Draw the star
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.size * 2)
        
        # Draw orbits and planets
        orbit_font = pygame.font.Font(None, 24)
        for i, planet in enumerate(self.planets):
            orbit_radius = 100 + planet['orbit_number'] * 60
            pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), orbit_radius, 1)
            
            # Calculate fixed planet position (no animation)
            # Distribute planets evenly around the orbit
            if 'x' not in planet or 'y' not in planet:
                angle = (i * 2 * math.pi / len(self.planets)) + math.pi/4  # Start from 45 degrees
                x = center_x + orbit_radius * math.cos(angle)
                y = center_y + orbit_radius * math.sin(angle)
                planet['x'] = x
                planet['y'] = y
            size = planet['size']
            
            # Draw the planet
            planet_color = PlanetProperties.PROPERTIES[planet['type']]['color']
            pygame.draw.circle(screen, planet_color, (int(planet['x']), int(planet['y'])), size)
            
            # Draw orbit number
            orbit_text = orbit_font.render(str(planet['orbit_number']), True, WHITE)
            orbit_rect = orbit_text.get_rect(
                center=(planet['x'], planet['y'] - size - 15)
            )
            # Draw text shadow
            shadow_text = orbit_font.render(str(planet['orbit_number']), True, GRAY)
            shadow_rect = shadow_text.get_rect(
                center=(planet['x'] + 0.5, planet['y'] - size - 14.5)
            )
            screen.blit(shadow_text, shadow_rect)
            screen.blit(orbit_text, orbit_rect)
