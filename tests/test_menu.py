"""Tests for the Menu system."""
import pytest
import pygame
import pygame_gui
from unittest.mock import MagicMock, patch
from game.menu import Menu, MenuItem
from game.enums import GameState
from game.resources import ResourceManager

@pytest.fixture
def resource_manager(mock_pygame):
    """Create a ResourceManager instance for testing."""
    return ResourceManager(mock_pygame, mock_pygame.font, mock_pygame.mixer, mock_pygame.display)

@pytest.fixture
def mock_ui_manager():
    """Create a mock UIManager for testing."""
    ui_manager = MagicMock(spec=pygame_gui.UIManager)
    return ui_manager

@pytest.fixture
def mock_ui_button():
    """Create a mock UIButton for testing."""
    button = MagicMock(spec=pygame_gui.elements.UIButton)
    return button

@pytest.fixture
def mock_ui_panel():
    """Create a mock UIPanel for testing."""
    panel = MagicMock(spec=pygame_gui.elements.UIPanel)
    return panel

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

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
@patch('pygame_gui.elements.UILabel')
def test_menu(mock_ui_label, mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test Menu initialization and functionality."""
    # Create menu items
    items = [
        MenuItem("Item 1", lambda: None),
        MenuItem("Item 2", lambda: None, enabled=False),
        MenuItem("Item 3", lambda: None)
    ]
    
    # Setup mocks
    mock_ui_button.return_value = MagicMock()
    mock_ui_panel.return_value = MagicMock()
    mock_ui_label.return_value = MagicMock()
    
    menu = Menu(items, "Test Menu", resource_manager)
    assert menu.title == "Test Menu"
    assert len(menu.items) == 3
    
    # Initialize menu with mock UI manager
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Show the menu first
    menu.show()
    
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
    """Test menu input handling before initialization."""
    menu = Menu([MenuItem("Test", lambda: None)], resource_manager=resource_manager)
    # Should return None when menu is not initialized
    assert menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})) is None

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
@patch('pygame_gui.elements.UILabel')
def test_menu_keyboard_activation(mock_ui_label, mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test menu item activation via keyboard."""
    activated = False
    def on_activate():
        nonlocal activated
        activated = True
        return "activated"

    # Setup mocks
    mock_ui_button.return_value = MagicMock()
    mock_ui_panel.return_value = MagicMock()
    mock_ui_label.return_value = MagicMock()

    menu = Menu([MenuItem("Test", on_activate)], resource_manager=resource_manager)
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Show the menu first
    menu.show()
    
    # Test enter key activation
    result = menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
    assert activated
    assert result == "activated"
    
    # Test disabled item
    activated = False
    menu = Menu([MenuItem("Test", on_activate, enabled=False)], resource_manager=resource_manager)
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Show the menu first
    menu.show()
    
    result = menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
    assert not activated
    assert result is None

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
@patch('pygame_gui.elements.UILabel')
def test_menu_selection_state(mock_ui_label, mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test menu selection state with keyboard navigation."""
    # Setup mocks
    mock_ui_button.return_value = MagicMock()
    mock_ui_panel.return_value = MagicMock()
    mock_ui_label.return_value = MagicMock()
    
    menu = Menu([
        MenuItem("Item 1", lambda: None),
        MenuItem("Item 2", lambda: None)
    ], resource_manager=resource_manager)
    
    # Initialize menu
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Show the menu first
    menu.show()
    
    # Initial state
    assert menu.selected_index == 0
    
    # Move selection down
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu.selected_index == 1
    
    # Test wrapping to top
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu.selected_index == 0
    
    # Test wrapping to bottom
    menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
    assert menu.selected_index == 1

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
@patch('pygame_gui.elements.UILabel')
def test_menu_title_initialization(mock_ui_label, mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test menu title initialization."""
    # Setup mocks
    mock_ui_button.return_value = MagicMock()
    mock_ui_panel.return_value = MagicMock()
    mock_ui_label.return_value = MagicMock()
    
    menu = Menu([MenuItem("Test", lambda: None)], "Menu Title", resource_manager)
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Verify that UILabel was created for the title
    mock_ui_label.assert_called()

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
def test_menu_button_click(mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test menu button click handling."""
    # Setup button click action
    activated = False
    def on_activate():
        nonlocal activated
        activated = True
        return "activated"
    
    # Create menu with mock button
    menu = Menu([MenuItem("Test", on_activate)], resource_manager=resource_manager)
    
    # Setup mock button
    mock_button = MagicMock()
    mock_ui_button.return_value = mock_button
    mock_panel = MagicMock()
    mock_ui_panel.return_value = mock_panel
    
    # Initialize menu
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Show the menu
    menu.show()
    assert menu.visible
    
    # Reset mock call counts
    mock_panel.hide.reset_mock()
    
    # Store the created button for reference
    button = menu.buttons[0]
    
    # Simulate button click event
    button_event = pygame.event.Event(
        pygame.USEREVENT, 
        {'user_type': pygame_gui.UI_BUTTON_PRESSED, 'ui_element': button}
    )
    
    # Handle the event
    result = menu.handle_input(button_event)
    
    # Verify the action was called
    assert activated
    assert result == "activated"
    
    # Verify the menu was hidden
    assert not menu.visible
    mock_panel.hide.assert_called_once()

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
def test_menu_keyboard_activation_hides_menu(mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test menu is hidden after keyboard activation."""
    activated = False
    def on_activate():
        nonlocal activated
        activated = True
        return "activated"

    # Setup mocks
    mock_ui_button.return_value = MagicMock()
    mock_panel = MagicMock()
    mock_ui_panel.return_value = mock_panel
    mock_ui_label = MagicMock()

    menu = Menu([MenuItem("Test", on_activate)], resource_manager=resource_manager)
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Show the menu
    menu.show()
    assert menu.visible
    
    # Reset mock call counts
    mock_panel.hide.reset_mock()
    
    # Test enter key activation
    result = menu.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
    assert activated
    assert result == "activated"
    
    # Verify the menu was hidden
    assert not menu.visible
    mock_panel.hide.assert_called_once()

@patch('pygame_gui.elements.UIButton')
@patch('pygame_gui.elements.UIPanel')
def test_menu_visibility_control(mock_ui_panel, mock_ui_button, mock_screen, resource_manager, mock_ui_manager):
    """Test menu show/hide functionality."""
    # Create menu
    menu = Menu([MenuItem("Test", lambda: None)], resource_manager=resource_manager)
    
    # Setup mocks
    mock_ui_button.return_value = MagicMock()
    mock_panel = MagicMock()
    mock_ui_panel.return_value = mock_panel
    
    # Initialize menu
    menu.initialize(mock_screen, mock_ui_manager)
    
    # Test show
    menu.show()
    assert menu.visible
    mock_panel.show.assert_called_once()
    
    # Reset mock call counts
    mock_panel.hide.reset_mock()
    
    # Test hide
    menu.hide()
    assert not menu.visible
    mock_panel.hide.assert_called_once()
    
    # Reset mock call counts
    mock_panel.show.reset_mock()
    
    # Test draw (should show the menu)
    menu.draw(mock_screen)
    assert menu.visible
    mock_panel.show.assert_called_once()
