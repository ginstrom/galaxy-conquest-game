"""Tests for the resource management system."""
import pytest
import pygame
import os
from game.resources import ResourceManager, TextCache
from tests.mocks import MockPygame, MockSurface, MockFont, MockSound

def test_singleton_pattern(mock_pygame):
    """Test that ResourceManager follows factory pattern."""
    manager1 = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    manager2 = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    assert manager1 is not manager2  # No longer a singleton

def test_load_image_success(mock_pygame):
    """Test successful image loading."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "planet1.png")
    image = manager.load_image("planet1", image_path)
    assert image is not None
    assert isinstance(image, MockSurface)
    assert "planet1" in manager.images

def test_load_image_failure(mock_pygame):
    """Test image loading failure handling."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    nonexistent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "nonexistent.png")
    image = manager.load_image("nonexistent", nonexistent_path)
    assert image is None
    assert "nonexistent" not in manager.images

def test_get_font(mock_pygame):
    """Test font creation and caching."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    font1 = manager.get_font(24)
    font2 = manager.get_font(24)
    assert font1 is font2  # Should return cached font
    assert isinstance(font1, MockFont)
    assert "24" in manager.fonts

def test_load_sound_success(mock_pygame):
    """Test successful sound loading."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    # Create a dummy sound for testing
    dummy_sound = MockSound(buffer=bytes([0]*44100))
    manager.sounds["test_sound"] = dummy_sound
    assert "test_sound" in manager.sounds
    assert isinstance(manager.sounds["test_sound"], MockSound)

def test_load_sound_failure(mock_pygame):
    """Test sound loading failure handling."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    nonexistent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds", "nonexistent.wav")
    sound = manager.load_sound("nonexistent", nonexistent_path)
    assert sound is None
    assert "nonexistent" not in manager.sounds

def test_cleanup(mock_pygame):
    """Test resource cleanup."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    # Load some resources
    font = manager.get_font(24)
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "planet1.png")
    image = manager.load_image("planet1", image_path)
    
    # Add a dummy sound for testing cleanup
    manager.sounds["test"] = MockSound(buffer=bytes([0]*44100))
    
    # Verify resources are loaded
    assert len(manager.fonts) > 0
    assert len(manager.images) > 0
    assert len(manager.sounds) > 0
    
    # Cleanup
    manager.cleanup()
    
    # Verify everything is cleared
    assert len(manager.fonts) == 0
    assert len(manager.images) == 0
    assert len(manager.sounds) == 0

def test_text_cache(mock_pygame):
    """Test TextCache functionality."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    text_cache = TextCache(manager)
    
    # Get text surface
    text = "Test Text"
    size = 24
    color = (255, 255, 255)
    surface1 = text_cache.get_text(text, size, color)
    
    # Verify it's a surface
    assert isinstance(surface1, MockSurface)
    
    # Get same text again - should return cached surface
    surface2 = text_cache.get_text(text, size, color)
    assert surface1 is surface2
    
    # Get different text - should return new surface
    surface3 = text_cache.get_text("Different", size, color)
    assert surface1 is not surface3
    
    # Clear cache
    text_cache.clear()
    surface4 = text_cache.get_text(text, size, color)
    assert surface1 is not surface4  # Should be new surface after clear

def test_text_cache_with_different_params(mock_pygame):
    """Test TextCache with different parameters."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    text_cache = TextCache(manager)
    
    text = "Test Text"
    size1, size2 = 24, 32
    color1, color2 = (255, 255, 255), (0, 0, 0)
    
    # Test different sizes
    surface1 = text_cache.get_text(text, size1, color1)
    surface2 = text_cache.get_text(text, size2, color1)
    assert surface1 is not surface2
    
    # Test different colors
    surface3 = text_cache.get_text(text, size1, color2)
    assert surface1 is not surface3

def test_resource_manager_initialization(mock_pygame):
    """Test ResourceManager initialization."""
    manager = ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)
    assert hasattr(manager, 'images')
    assert hasattr(manager, 'fonts')
    assert hasattr(manager, 'sounds')
    assert hasattr(manager, 'text_cache')
    assert isinstance(manager.text_cache, TextCache)
