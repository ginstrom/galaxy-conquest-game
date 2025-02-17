"""Tests for the Menu system."""
import pytest
import pygame
from game.menu import Menu, MenuItem
from game.enums import GameState
from game.resources import ResourceManager

@pytest.fixture
def resource_manager(mock_pygame):
    """Create a ResourceManager instance for testing."""
    return ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)

@pytest.fixture
def mock_screen():
    """Create a mock screen for testing."""
    from tests.mocks import MockSurface
    return MockSurface((800, 600))

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

def test_menu(mock_screen, resource_manager):
    """Test Menu initialization and functionality."""
    # Create menu items
    items = [
        MenuItem("Item 1", lambda: None),
        MenuItem("Item 2", lambda: None, enabled=False),
        MenuItem("Item 3", lambda: None)
    ]
    
    menu = Menu(items, "Test Menu", resource_manager)
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

def test_menu_screen_guard(resource_manager):
    """Test menu input handling before screen initialization."""
    menu = Menu([MenuItem("Test", lambda: None)], resource_manager=resource_manager)
    # Should return None when screen is not initialized
    assert menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})) is None

def test_menu_keyboard_activation(mock_screen, resource_manager):
    """Test menu item activation via keyboard."""
    activated = False
    def on_activate():
        nonlocal activated
        activated = True
        return "activated"

    menu = Menu([MenuItem("Test", on_activate)], resource_manager=resource_manager)
    menu.draw(mock_screen)
    
    # Test enter key activation
    result = menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
    assert activated
    assert result == "activated"
    
    # Test disabled item
    activated = False
    menu = Menu([MenuItem("Test", on_activate, enabled=False)], resource_manager=resource_manager)
    menu.draw(mock_screen)
    result = menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
    assert not activated
    assert result is None

def test_menu_visual_state(mock_screen, resource_manager):
    """Test menu visual state including selection indicators."""
    menu = Menu([
        MenuItem("Item 1", lambda: None),
        MenuItem("Item 2", lambda: None)
    ], resource_manager=resource_manager)
    
    # Initial state
    menu.draw(mock_screen)
    assert menu.items[0].selected  # First item should be selected
    assert not menu.items[1].selected
    
    # Move selection down
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    menu.draw(mock_screen)
    assert not menu.items[0].selected
    assert menu.items[1].selected
    
    # Test wrapping to top
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    menu.draw(mock_screen)
    assert menu.items[0].selected
    assert not menu.items[1].selected
    
    # Test wrapping to bottom
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
    menu.draw(mock_screen)
    assert not menu.items[0].selected
    assert menu.items[1].selected

def test_menu_title_drawing(mock_screen, resource_manager):
    """Test menu title drawing."""
    menu = Menu([MenuItem("Test", lambda: None)], "Menu Title", resource_manager)
    menu.draw(mock_screen)
    # Title drawing is tested implicitly since it would raise an error if it failed
