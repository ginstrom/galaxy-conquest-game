"""Tests for the Menu system."""
import pytest
import pygame
from game.menu import Menu, MenuItem
from game.enums import GameState

# Initialize pygame for testing
pygame.init()

@pytest.fixture
def mock_screen():
    """Create a mock screen for testing."""
    return pygame.Surface((800, 600))

def test_menu_item():
    """Test MenuItem initialization and callback."""
    callback_called = False
    
    def test_callback():
        nonlocal callback_called
        callback_called = True
    
    item = MenuItem("Test Item", test_callback)
    assert item.text == "Test Item"
    assert item.enabled  # Default should be enabled
    
    # Test callback
    item.action()
    assert callback_called

def test_menu(mock_screen):
    """Test Menu initialization and functionality."""
    # Create menu items
    items = [
        MenuItem("Item 1", lambda: None),
        MenuItem("Item 2", lambda: None, enabled=False),
        MenuItem("Item 3", lambda: None)
    ]
    
    menu = Menu(items, "Test Menu")
    assert menu.title == "Test Menu"
    assert len(menu.items) == 3
    
    # Draw menu to initialize screen
    menu.draw(mock_screen)
    
    # Test selection with keyboard input
    assert menu.selected_index == 0
    
    # Simulate pressing down key
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu.selected_index == 1
    
    # Simulate pressing down key again
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu.selected_index == 2
    
    # Simulate pressing up key
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
    assert menu.selected_index == 1
