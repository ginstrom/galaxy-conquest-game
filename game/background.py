"""
Background effects for Galaxy Conquest.

This module handles the generation and rendering of background visual effects:
- Twinkling stars with varying brightness
- Colorful nebulae using particle systems
- Different background styles for galaxy and system views

The effects are designed to create an immersive space atmosphere while
maintaining performance through optimized rendering techniques.
"""

import random
import math
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, NUM_BACKGROUND_STARS,
    NUM_NEBULAE, RED, BLUE, PURPLE, PINK
)

class BackgroundEffect:
    """
    Manages and renders background visual effects for the game.
    
    Creates and maintains two types of effects:
    1. Stars: Small points of light that twinkle over time
    2. Nebulae: Large, colorful gas clouds created using particle systems
    
    The effects are rendered differently in galaxy and system views to create
    distinct atmospheric experiences for each game state.
    """
    
    def __init__(self):
        # Generate background stars with twinkling properties
        self.stars = []
        for _ in range(NUM_BACKGROUND_STARS):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 2)
            # Base brightness range 100-180 gives visible but not overpowering stars
            brightness = random.randint(100, 180)
            # Store star properties including position, appearance, and twinkling data
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
            # Use 40 particles per nebula for good visual density while maintaining performance
            num_particles = 40
            # Each particle represents a portion of the nebula gas cloud
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
        """
        Draw the background for galaxy view.
        
        Renders both nebulae and stars to create a rich space environment.
        Nebulae are drawn first as a base layer, with twinkling stars overlaid.
        Each star's brightness varies sinusoidally over time for a dynamic effect.
        
        Args:
            screen: Pygame surface to draw on
        """
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
        # Convert milliseconds to seconds for smoother twinkling calculations
        current_time = pygame.time.get_ticks() / 1000
        for star in self.stars:
            # Calculate twinkling effect:
            # - Multiply time by 2 for faster oscillation
            # - Add offset for varied timing between stars
            # - Multiply by 20 for visible but subtle brightness range
            brightness_variation = math.sin(current_time * 2 + star['twinkle_offset']) * 20
            color = list(star['color'])
            # Apply brightness variation to all RGB components for consistent color
            for i in range(3):
                color[i] = max(0, min(255, color[i] + brightness_variation))
            
            pygame.draw.circle(
                screen,
                color,
                (star['x'], star['y']),
                star['size']
            )

    def draw_system_background(self, screen):
        """
        Draw the background for system view.
        
        Renders only the star field without nebulae for a cleaner view when
        examining individual star systems. Stars still maintain their twinkling
        effect to keep the background dynamic.
        
        Args:
            screen: Pygame surface to draw on
        """
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
