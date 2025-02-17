"""Resource management system for Galaxy Conquest."""

import pygame
import os
from typing import Dict, Optional
import logging

# Setup logging
logger = logging.getLogger(__name__)

class ResourceManagerFactory:
    """Factory class for creating ResourceManager instances with real pygame."""
    @staticmethod
    def create():
        """Create a ResourceManager instance with real pygame modules."""
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
            try:
                pygame.display.set_mode((1, 1), pygame.HIDDEN)
            except pygame.error:
                os.environ['SDL_VIDEODRIVER'] = 'dummy'
                pygame.display.init()
                pygame.display.set_mode((1, 1))
        if not pygame.font.get_init():
            pygame.font.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init(44100, -16, 2, 2048)
            
        return ResourceManager(pygame, pygame.font, pygame.mixer, pygame.display)

class ResourceManager:
    """Resource management system for the game."""
    def __init__(self, pygame_module, font_module, mixer_module, display_module):
        """Initialize the resource manager with provided modules."""
        self.pygame = pygame_module
        self.font = font_module
        self.mixer = mixer_module
        self.display = display_module
        
        self.images: Dict[str, pygame.Surface] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.text_cache = TextCache(self)
        logger.info("ResourceManager initialized with provided modules")

    def load_image(self, name: str, path: str) -> Optional[pygame.Surface]:
        """Load an image and store it in the cache."""
        if not self.display.get_init():
            logger.error("Display system not initialized")
            return None

        try:
            if name not in self.images:
                logger.debug(f"Loading image: {path}")
                try:
                    image = self.pygame.image.load(path)
                    if image.get_alpha():
                        image = image.convert_alpha()
                    else:
                        image = image.convert()
                    self.images[name] = image
                except (self.pygame.error, FileNotFoundError) as e:
                    logger.error(f"Error loading image {path}: {e}")
                    return None
            return self.images[name]
        except Exception as e:
            logger.error(f"Unexpected error loading image {path}: {e}")
            return None

    def get_font(self, size: int, name: Optional[str] = None) -> pygame.font.Font:
        """Get a font of specified size from cache or create new."""
        if not self.font.get_init():
            logger.error("Font system not initialized")
            raise self.pygame.error("Font system not initialized")
            
        key = f"{name}_{size}" if name else str(size)
        if key not in self.fonts:
            try:
                logger.debug(f"Creating font: {name} size {size}")
                if name is None:
                    # Use default system font when no font name is provided
                    self.fonts[key] = self.font.SysFont(None, size)
                else:
                    self.fonts[key] = self.font.Font(name, size)
            except self.pygame.error as e:
                logger.error(f"Failed to create font (size={size}, name={name}): {e}")
                raise
        return self.fonts[key]

    def load_sound(self, name: str, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound and store it in the cache."""
        if not self.mixer.get_init():
            logger.error("Mixer system not initialized")
            return None

        try:
            if name not in self.sounds:
                logger.debug(f"Loading sound: {path}")
                try:
                    self.sounds[name] = self.mixer.Sound(path)
                except (self.pygame.error, FileNotFoundError) as e:
                    logger.error(f"Error loading sound {path}: {e}")
                    return None
            return self.sounds[name]
        except Exception as e:
            logger.error(f"Unexpected error loading sound {path}: {e}")
            return None

    def cleanup(self):
        """Clean up all loaded resources."""
        logger.info("Cleaning up resources")
        # Clear image surfaces
        for image in self.images.values():
            image.set_alpha(None)
        self.images.clear()
        
        # Clear fonts
        self.fonts.clear()
        
        # Stop and clear sounds
        for sound in self.sounds.values():
            sound.stop()
        self.sounds.clear()
        
        # Clear text cache
        self.text_cache.clear()

class TextCache:
    """Cache for rendered text surfaces to avoid frequent re-rendering."""
    def __init__(self, resource_manager: ResourceManager):
        self.resource_manager = resource_manager
        self.cache: Dict[str, pygame.Surface] = {}
        
    def get_text(self, text: str, size: int, color: tuple, 
                 font_name: Optional[str] = None) -> pygame.Surface:
        """Get rendered text surface from cache or render new."""
        key = f"{text}_{size}_{color}_{font_name}"
        if key not in self.cache:
            font = self.resource_manager.get_font(size, font_name)
            self.cache[key] = font.render(text, True, color)
        return self.cache[key]
    
    def clear(self):
        """Clear the text cache."""
        self.cache.clear()
