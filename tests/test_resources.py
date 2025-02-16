"""Tests for the resource management system."""
import pytest
import pygame
import os
from game.resources import ResourceManager, TextCache

# Initialize pygame for testing
pygame.init()
pygame.mixer.init()

@pytest.fixture
def resource_manager():
    """Create a resource manager instance for testing."""
    manager = ResourceManager()
    yield manager
    # Cleanup after each test
    manager.cleanup()

def test_singleton_pattern():
    """Test that ResourceManager follows singleton pattern."""
    manager1 = ResourceManager()
    manager2 = ResourceManager()
    assert manager1 is manager2

def test_load_image_success(resource_manager):
    """Test successful image loading."""
    # Use a known image from the project
    image_path = os.path.join("img", "planet1.png")
    image = resource_manager.load_image("planet1", image_path)
    assert image is not None
    assert isinstance(image, pygame.Surface)
    # Check it's cached
    assert "planet1" in resource_manager.images

def test_load_image_failure(resource_manager):
    """Test image loading failure handling."""
    # Try to load non-existent image
    nonexistent_path = os.path.join("img", "nonexistent.png")
    image = resource_manager.load_image("nonexistent", nonexistent_path)
    assert image is None
    assert "nonexistent" not in resource_manager.images

def test_get_font(resource_manager):
    """Test font creation and caching."""
    font1 = resource_manager.get_font(24)
    font2 = resource_manager.get_font(24)
    assert font1 is font2  # Should return cached font
    assert isinstance(font1, pygame.font.Font)
    assert "24" in resource_manager.fonts

def test_load_sound_success(resource_manager):
    """Test successful sound loading."""
    # Create a dummy sound for testing
    dummy_sound = pygame.mixer.Sound(buffer=bytes([0]*44100))
    resource_manager.sounds["test_sound"] = dummy_sound
    assert "test_sound" in resource_manager.sounds
    assert isinstance(resource_manager.sounds["test_sound"], pygame.mixer.Sound)

def test_load_sound_failure(resource_manager):
    """Test sound loading failure handling."""
    nonexistent_path = os.path.join("sounds", "nonexistent.wav")
    sound = resource_manager.load_sound("nonexistent", nonexistent_path)
    assert sound is None
    assert "nonexistent" not in resource_manager.sounds

def test_cleanup(resource_manager):
    """Test resource cleanup."""
    # Load some resources
    font = resource_manager.get_font(24)
    image_path = os.path.join("img", "planet1.png")
    image = resource_manager.load_image("planet1", image_path)
    
    # Add a dummy sound for testing cleanup
    resource_manager.sounds["test"] = pygame.mixer.Sound(buffer=bytes([0]*44100))
    
    # Verify resources are loaded
    assert len(resource_manager.fonts) > 0
    assert len(resource_manager.images) > 0
    assert len(resource_manager.sounds) > 0
    
    # Cleanup
    resource_manager.cleanup()
    
    # Verify everything is cleared
    assert len(resource_manager.fonts) == 0
    assert len(resource_manager.images) == 0
    assert len(resource_manager.sounds) == 0

def test_text_cache():
    """Test TextCache functionality."""
    manager = ResourceManager()
    text_cache = TextCache(manager)
    
    # Get text surface
    text = "Test Text"
    size = 24
    color = (255, 255, 255)
    surface1 = text_cache.get_text(text, size, color)
    
    # Verify it's a surface
    assert isinstance(surface1, pygame.Surface)
    
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

def test_text_cache_with_different_params():
    """Test TextCache with different parameters."""
    manager = ResourceManager()
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

def test_resource_manager_initialization():
    """Test ResourceManager initialization."""
    manager = ResourceManager()
    assert hasattr(manager, 'images')
    assert hasattr(manager, 'fonts')
    assert hasattr(manager, 'sounds')
    assert hasattr(manager, 'text_cache')
    assert isinstance(manager.text_cache, TextCache)
    assert manager.initialized
