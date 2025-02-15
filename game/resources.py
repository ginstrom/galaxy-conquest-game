"""Resource management system for Galaxy Conquest."""

import pygame
import os
from typing import Dict, Optional
import logging

# Setup logging
logger = logging.getLogger(__name__)

class ResourceManager:
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one resource manager exists."""
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the resource manager if not already initialized."""
        if not hasattr(self, 'initialized'):
            self.images: Dict[str, pygame.Surface] = {}
            self.fonts: Dict[str, pygame.font.Font] = {}
            self.sounds: Dict[str, pygame.mixer.Sound] = {}
            self.text_cache = TextCache(self)
            self.initialized = True
            logger.info("ResourceManager initialized")

    def load_image(self, name: str, path: str) -> Optional[pygame.Surface]:
        """Load an image and store it in the cache."""
        try:
            if name not in self.images:
                logger.debug(f"Loading image: {path}")
                try:
                    image = pygame.image.load(path)
                    if image.get_alpha():
                        image = image.convert_alpha()
                    else:
                        image = image.convert()
                    self.images[name] = image
                except (pygame.error, FileNotFoundError) as e:
                    logger.error(f"Error loading image {path}: {e}")
                    return None
            return self.images[name]
        except Exception as e:
            logger.error(f"Unexpected error loading image {path}: {e}")
            return None

    def get_font(self, size: int, name: Optional[str] = None) -> pygame.font.Font:
        """Get a font of specified size from cache or create new."""
        key = f"{name}_{size}" if name else str(size)
        if key not in self.fonts:
            logger.debug(f"Creating font: {name} size {size}")
            self.fonts[key] = pygame.font.Font(name, size)
        return self.fonts[key]

    def load_sound(self, name: str, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound and store it in the cache."""
        try:
            if name not in self.sounds:
                logger.debug(f"Loading sound: {path}")
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except (pygame.error, FileNotFoundError) as e:
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
