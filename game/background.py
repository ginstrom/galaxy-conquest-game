"""Background effects for Galaxy Conquest."""

import random
import math
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, NUM_BACKGROUND_STARS,
    NUM_NEBULAE, RED, BLUE, PURPLE, PINK
)

class BackgroundEffect:
    def __init__(self):
        # Generate background stars
        self.stars = []
        for _ in range(NUM_BACKGROUND_STARS):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 2)
            brightness = random.randint(100, 180)  # Reduced brightness range
            self.stars.append({
                'x': x,
                'y': y,
                'size': size,
                'color': (brightness, brightness, brightness),
                'twinkle_offset': random.uniform(0, 2 * math.pi)  # For smoother twinkling
            })
        
        # Generate nebulae
        self.nebulae = []
        nebula_colors = [(RED[0], 0, RED[2], 20),      # Reduced alpha
                        (0, 0, BLUE[2], 20),           # Reduced alpha
                        (PURPLE[0], 0, PURPLE[2], 20), # Reduced alpha
                        (PINK[0], PINK[1], PINK[2], 20)]  # Reduced alpha
        
        for _ in range(NUM_NEBULAE):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(100, 200)
            color = random.choice(nebula_colors)
            num_particles = 40  # Reduced number of particles
            particles = []
            
            for _ in range(num_particles):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, size)
                px = x + distance * math.cos(angle)
                py = y + distance * math.sin(angle)
                particle_size = random.randint(20, 35)  # Slightly reduced size range
                particles.append({
                    'x': px,
                    'y': py,
                    'size': particle_size
                })
            
            self.nebulae.append({
                'x': x,
                'y': y,
                'size': size,
                'color': color,
                'particles': particles
            })

    def draw_galaxy_background(self, screen):
        """Draw the background for galaxy view."""
        # Draw nebulae
        for nebula in self.nebulae:
            # Create a surface for the nebula
            nebula_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for particle in nebula['particles']:
                pygame.draw.circle(
                    nebula_surface,
                    nebula['color'],
                    (int(particle['x']), int(particle['y'])),
                    particle['size']
                )
            screen.blit(nebula_surface, (0, 0))
        
        # Draw stars with twinkling effect
        current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
        for star in self.stars:
            # Calculate brightness variation
            brightness_variation = math.sin(current_time * 2 + star['twinkle_offset']) * 20
            color = list(star['color'])
            for i in range(3):  # Modify all RGB components
                color[i] = max(0, min(255, color[i] + brightness_variation))
            
            pygame.draw.circle(
                screen,
                color,
                (star['x'], star['y']),
                star['size']
            )

    def draw_system_background(self, screen):
        """Draw the background for system view."""
        # Only draw stars in system view
        current_time = pygame.time.get_ticks() / 1000
        for star in self.stars:
            brightness_variation = math.sin(current_time * 2 + star['twinkle_offset']) * 20
            color = list(star['color'])
            for i in range(3):
                color[i] = max(0, min(255, color[i] + brightness_variation))
            
            pygame.draw.circle(
                screen,
                color,
                (star['x'], star['y']),
                star['size']
            )
