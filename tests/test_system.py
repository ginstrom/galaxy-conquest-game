"""Tests for the SystemView class."""

import pytest
import pygame
from unittest.mock import MagicMock, patch

from game.views.system import SystemView
from game.enums import GameState, PlanetType, ResourceType
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from tests.mocks import MockGame, MockSurface

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup and cleanup pygame for each test."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

@pytest.fixture
def mock_game():
    """Create a mock game instance for testing."""
    return MockGame()

@pytest.fixture
def mock_screen():
    """Create a mock screen surface for testing."""
    return MockSurface((SCREEN_WIDTH, SCREEN_HEIGHT))

@pytest.fixture
def system_view(mock_game, monkeypatch):
    """Create a SystemView instance for testing."""
    # Mock the SystemViewInfoPanel class to avoid pygame_gui initialization
    mock_panel = MagicMock()
    mock_panel.panel_width = 300
    
    # Create a mock class for SystemViewInfoPanel
    MockSystemViewInfoPanel = MagicMock(return_value=mock_panel)
    
    # Patch the SystemViewInfoPanel import in system.py
    monkeypatch.setattr('game.views.system.SystemViewInfoPanel', MockSystemViewInfoPanel)
    
    # Now create the SystemView instance
    view = SystemView(mock_game)
    
    # Ensure the view has the mock panel
    view.panel = mock_panel
    
    return view

class TestSystemViewInitialization:
    """Tests for SystemView initialization."""
    
    def test_initialization(self, mock_game, monkeypatch):
        """Test that SystemView initializes correctly."""
        # Mock the SystemViewInfoPanel class to avoid pygame_gui initialization
        mock_panel = MagicMock()
        mock_panel.panel_width = 300
        
        # Create a mock class for SystemViewInfoPanel
        MockSystemViewInfoPanel = MagicMock(return_value=mock_panel)
        
        # Patch the SystemViewInfoPanel import in system.py
        monkeypatch.setattr('game.views.system.SystemViewInfoPanel', MockSystemViewInfoPanel)
        
        # Now create the SystemView instance
        view = SystemView(mock_game)
        
        # Ensure the view has the mock panel
        view.panel = mock_panel
        
        assert view.game == mock_game
        assert view.panel is not None
        assert view.available_width == SCREEN_WIDTH - view.panel.panel_width
        assert view.center_x == view.available_width // 2
        assert view.center_y == SCREEN_HEIGHT // 2
        assert view.menu is not None
        assert len(view.menu.items) == 3  # Check that menu has 3 items

class TestSystemViewKeyHandling:
    """Tests for SystemView key handling."""
    
    def test_handle_keydown_escape(self, system_view, mock_game):
        """Test that pressing escape transitions to SYSTEM_MENU state."""
        # Create a mock event with escape key
        event = MagicMock()
        event.key = pygame.K_ESCAPE
        
        # Handle the key event
        system_view.handle_keydown(event)
        
        # Verify that to_state was called with the correct parameters
        mock_game.to_state.assert_called_once_with(GameState.SYSTEM, GameState.SYSTEM_MENU)
    
    def test_handle_keydown_other_key(self, system_view, mock_game):
        """Test handling of non-escape keys."""
        # Set initial state
        mock_game.state = GameState.SYSTEM
        
        # Create a mock event with a non-escape key
        event = MagicMock()
        event.key = pygame.K_SPACE
        
        # Handle the key event
        system_view.handle_keydown(event)
        
        # Verify that the game state did not change
        assert mock_game.state == GameState.SYSTEM

class TestSystemViewMouseHandling:
    """Tests for SystemView mouse handling."""
    
    def test_handle_click_no_selected_system(self, system_view, mock_game):
        """Test handling of clicks when no system is selected."""
        # Ensure no system is selected
        mock_game.selected_system = None
        
        # Store the initial selected planet
        initial_planet = mock_game.selected_planet
        
        # Position inside the system view area
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the click
        system_view.handle_click(pos)
        
        # Verify that the selected planet didn't change
        assert mock_game.selected_planet == initial_planet
    
    def test_handle_click_on_planet(self, system_view, mock_game):
        """Test handling of clicks on a planet."""
        # Create a mock system with planets
        system = MagicMock()
        planet = {
            'name': 'Test Planet',
            'x': 100,
            'y': 100,
            'size': 20,
            'type': PlanetType.TERRESTRIAL,
            'resources': []
        }
        system.planets = [planet]
        mock_game.selected_system = system
        
        # Position inside the planet's radius
        pos = (100, 100)
        
        # Handle the click
        system_view.handle_click(pos)
        
        # Verify that the planet was selected and to_state was called
        assert mock_game.selected_planet == planet
        mock_game.to_state.assert_called_once_with(GameState.SYSTEM, GameState.PLANET)
    
    def test_handle_click_not_on_planet(self, system_view, mock_game):
        """Test handling of clicks not on any planet."""
        # Create a mock system with planets
        system = MagicMock()
        planet = {
            'name': 'Test Planet',
            'x': 100,
            'y': 100,
            'size': 20,
            'type': PlanetType.TERRESTRIAL,
            'resources': []
        }
        system.planets = [planet]
        mock_game.selected_system = system
        
        # Clear the selected planet
        mock_game.selected_planet = None
        
        # Position not inside any planet's radius
        pos = (200, 200)
        
        # Handle the click
        system_view.handle_click(pos)
        
        # Verify that no planet was selected
        assert mock_game.selected_planet is None
    
    def test_handle_click_on_planet_without_coordinates(self, system_view, mock_game):
        """Test handling of clicks when a planet doesn't have coordinates."""
        # Create a mock system with planets
        system = MagicMock()
        planet = {
            'name': 'Test Planet',
            'type': PlanetType.TERRESTRIAL,
            'resources': []
        }
        system.planets = [planet]
        mock_game.selected_system = system
        
        # Clear the selected planet
        mock_game.selected_planet = None
        
        # Position inside the system view area
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the click
        system_view.handle_click(pos)
        
        # Verify that no planet was selected
        assert mock_game.selected_planet is None
    
    def test_handle_right_click_no_selected_system(self, system_view, mock_game):
        """Test handling of right clicks when no system is selected."""
        # Ensure no system is selected
        mock_game.selected_system = None
        
        # Position inside the system view area
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the right click
        system_view.handle_right_click(pos)
        
        # Verify that the game state did not change
        assert mock_game.state != GameState.SYSTEM_MENU
    
    def test_handle_right_click_with_selected_system(self, system_view, mock_game):
        """Test handling of right clicks when a system is selected."""
        # Create a mock system
        system = MagicMock()
        mock_game.selected_system = system
        
        # Position inside the system view area
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the right click
        system_view.handle_right_click(pos)
        
        # Verify that the selected planet is None and to_state was called
        assert mock_game.selected_planet is None
        mock_game.to_state.assert_called_once_with(GameState.SYSTEM, GameState.SYSTEM_MENU)

class TestSystemViewUpdate:
    """Tests for SystemView update method."""
    
    def test_update_no_selected_system(self, system_view, mock_game):
        """Test update when no system is selected."""
        # Ensure no system is selected
        mock_game.selected_system = None
        
        # Update the view
        system_view.update()
        
        # Verify that hovered_planet is None
        assert mock_game.hovered_planet is None
    
    def test_update_not_in_system_state(self, system_view, mock_game):
        """Test update when not in SYSTEM state."""
        # Create a mock system
        system = MagicMock()
        mock_game.selected_system = system
        mock_game.state = GameState.GALAXY
        
        # Update the view
        system_view.update()
        
        # Verify that hovered_planet is None
        assert mock_game.hovered_planet is None
    
    @patch('pygame.mouse.get_pos')
    def test_update_mouse_over_planet(self, mock_get_pos, system_view, mock_game):
        """Test update when mouse is over a planet."""
        # Create a mock system with planets
        system = MagicMock()
        planet = {
            'name': 'Test Planet',
            'x': 100,
            'y': 100,
            'size': 20,
            'type': PlanetType.TERRESTRIAL,
            'resources': []
        }
        system.planets = [planet]
        mock_game.selected_system = system
        mock_game.state = GameState.SYSTEM
        
        # Mock mouse position over the planet
        mock_get_pos.return_value = (100, 100)
        
        # Update the view
        system_view.update()
        
        # Verify that hovered_planet is set to the planet
        assert mock_game.hovered_planet == planet
    
    @patch('pygame.mouse.get_pos')
    def test_update_mouse_not_over_planet(self, mock_get_pos, system_view, mock_game):
        """Test update when mouse is not over any planet."""
        # Create a mock system with planets
        system = MagicMock()
        planet = {
            'name': 'Test Planet',
            'x': 100,
            'y': 100,
            'size': 20,
            'type': PlanetType.TERRESTRIAL,
            'resources': []
        }
        system.planets = [planet]
        mock_game.selected_system = system
        mock_game.state = GameState.SYSTEM
        
        # Mock mouse position not over any planet
        mock_get_pos.return_value = (200, 200)
        
        # Update the view
        system_view.update()
        
        # Verify that hovered_planet is None
        assert mock_game.hovered_planet is None
    
    @patch('pygame.mouse.get_pos')
    def test_update_mouse_over_info_panel(self, mock_get_pos, system_view, mock_game):
        """Test update when mouse is over the info panel."""
        # Create a mock system with planets
        system = MagicMock()
        planet = {
            'name': 'Test Planet',
            'x': 100,
            'y': 100,
            'size': 20,
            'type': PlanetType.TERRESTRIAL,
            'resources': []
        }
        system.planets = [planet]
        mock_game.selected_system = system
        mock_game.state = GameState.SYSTEM
        
        # Mock mouse position over the info panel
        mock_get_pos.return_value = (SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2)
        
        # Update the view
        system_view.update()
        
        # Verify that hovered_planet is None
        assert mock_game.hovered_planet is None

class TestSystemViewDrawing:
    """Tests for SystemView drawing."""
    
    def test_draw_with_selected_system(self, system_view, mock_game, mock_screen):
        """Test drawing with a selected system."""
        # Create a mock system
        system = MagicMock()
        mock_game.selected_system = system
        mock_game.state = GameState.SYSTEM
        
        # Mock the background and panel draw methods
        mock_game.background.draw_system_background = MagicMock()
        system_view.panel.draw = MagicMock()
        
        # Draw the view
        system_view.draw(mock_screen)
        
        # Verify that the background, system, and panel were drawn
        mock_game.background.draw_system_background.assert_called_once_with(mock_screen)
        system.draw_system_view.assert_called_once_with(mock_screen)
        system_view.panel.draw.assert_called_once_with(mock_screen)
    
    def test_draw_without_selected_system(self, system_view, mock_game, mock_screen):
        """Test drawing without a selected system."""
        # Ensure no system is selected
        mock_game.selected_system = None
        
        # Mock the background draw method
        mock_game.background.draw_system_background = MagicMock()
        
        # Draw the view
        system_view.draw(mock_screen)
        
        # Verify that the background was drawn and to_state was called
        mock_game.background.draw_system_background.assert_called_once_with(mock_screen)
        mock_game.to_state.assert_called_once_with(GameState.SYSTEM, GameState.GALAXY)
    
    def test_draw_in_menu_state(self, system_view, mock_game, mock_screen):
        """Test drawing in menu state."""
        # Create a mock system
        system = MagicMock()
        mock_game.selected_system = system
        mock_game.state = GameState.SYSTEM_MENU
        
        # Mock the background and panel draw methods
        mock_game.background.draw_system_background = MagicMock()
        system_view.panel.draw = MagicMock()
        
        # Draw the view
        system_view.draw(mock_screen)
        
        # Verify that the background, system, and panel were drawn
        # Note: Menu drawing is now handled by the game loop, not in the view's draw method
        mock_game.background.draw_system_background.assert_called_once_with(mock_screen)
        system.draw_system_view.assert_called_once_with(mock_screen)
        system_view.panel.draw.assert_called_once_with(mock_screen)
