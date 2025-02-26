"""Tests for the GalaxyView class."""

import pytest
import pygame
from unittest.mock import MagicMock, patch

from game.views.galaxy import GalaxyView
from game.enums import GameState
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
def galaxy_view(mock_game):
    """Create a GalaxyView instance for testing."""
    return GalaxyView(mock_game)

class TestGalaxyViewInitialization:
    """Tests for GalaxyView initialization."""
    
    def test_initialization(self, mock_game):
        """Test that GalaxyView initializes correctly."""
        view = GalaxyView(mock_game)
        
        assert view.game == mock_game
        assert view.panel is not None
        assert view.galaxy_rect.width == SCREEN_WIDTH - view.panel.panel_width
        assert view.galaxy_rect.height == SCREEN_HEIGHT
        assert view.menu is not None
        assert len(view.menu.items) == 5  # Check that menu has 5 items

class TestGalaxyViewKeyHandling:
    """Tests for GalaxyView key handling."""
    
    def test_handle_keydown_escape(self, galaxy_view, mock_game):
        """Test that pressing escape transitions to GALAXY_MENU state."""
        # Create a mock event with escape key
        event = MagicMock()
        event.key = pygame.K_ESCAPE
        
        # Handle the key event
        galaxy_view.handle_keydown(event)
        
        # Verify that the game state changed to GALAXY_MENU
        assert mock_game.state == GameState.GALAXY_MENU
    
    def test_handle_keydown_other_key(self, galaxy_view, mock_game):
        """Test handling of non-escape keys."""
        # Set initial state
        mock_game.state = GameState.GALAXY
        
        # Create a mock event with a non-escape key
        event = MagicMock()
        event.key = pygame.K_SPACE
        
        # Handle the key event
        galaxy_view.handle_keydown(event)
        
        # Verify that the game state did not change
        assert mock_game.state == GameState.GALAXY

class TestGalaxyViewMouseHandling:
    """Tests for GalaxyView mouse handling."""
    
    def test_handle_click_outside_galaxy_rect(self, galaxy_view, mock_game):
        """Test handling of clicks outside the galaxy rectangle."""
        # Position outside the galaxy rectangle (in the info panel area)
        pos = (SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2)
        
        # Store the initial selected system
        initial_system = mock_game.selected_system
        
        # Handle the click
        galaxy_view.handle_click(pos)
        
        # Verify that the selected system didn't change
        assert mock_game.selected_system == initial_system
    
    def test_handle_click_on_system(self, galaxy_view, mock_game):
        """Test handling of clicks on a star system."""
        # Create a mock star system
        system = MagicMock()
        system.name = "Test System"
        system.rect = pygame.Rect(100, 100, 50, 50)
        mock_game.star_systems = [system]
        
        # Position inside the system's rect
        pos = (125, 125)
        
        # Handle the click
        galaxy_view.handle_click(pos)
        
        # Verify that the system was selected and state changed
        assert mock_game.selected_system == system
        assert mock_game.state == GameState.SYSTEM
        assert mock_game.current_view == mock_game.system_view
    
    def test_handle_click_not_on_system(self, galaxy_view, mock_game):
        """Test handling of clicks not on any star system."""
        # Create a mock star system
        system = MagicMock()
        system.name = "Test System"
        system.rect = pygame.Rect(100, 100, 50, 50)
        mock_game.star_systems = [system]
        
        # Clear the selected system
        mock_game.selected_system = None
        
        # Position not inside any system's rect
        pos = (200, 200)
        
        # Handle the click
        galaxy_view.handle_click(pos)
        
        # Verify that no system was selected
        assert mock_game.selected_system is None
    
    def test_handle_right_click_outside_galaxy_rect(self, galaxy_view, mock_game):
        """Test handling of right clicks outside the galaxy rectangle."""
        # Position outside the galaxy rectangle (in the info panel area)
        pos = (SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2)
        
        # Handle the right click
        galaxy_view.handle_right_click(pos)
        
        # Verify that the game state did not change
        assert mock_game.state != GameState.GALAXY_MENU
    
    def test_handle_right_click_inside_galaxy_rect(self, galaxy_view, mock_game):
        """Test handling of right clicks inside the galaxy rectangle."""
        # Position inside the galaxy rectangle
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the right click
        galaxy_view.handle_right_click(pos)
        
        # Verify that the game state changed to GALAXY_MENU
        assert mock_game.selected_system is None
        assert mock_game.state == GameState.GALAXY_MENU

class TestGalaxyViewDrawing:
    """Tests for GalaxyView drawing."""
    
    def test_draw_normal_state(self, galaxy_view, mock_game, mock_screen):
        """Test drawing in normal state."""
        # Set up mock game state
        mock_game.state = GameState.GALAXY
        mock_game.star_systems = [MagicMock(), MagicMock()]
        
        # Mock the background and panel draw methods
        mock_game.background.draw_galaxy_background = MagicMock()
        galaxy_view.panel.draw = MagicMock()
        
        # Draw the view
        galaxy_view.draw(mock_screen)
        
        # Verify that the background and panel were drawn
        mock_game.background.draw_galaxy_background.assert_called_once_with(mock_screen)
        galaxy_view.panel.draw.assert_called_once_with(mock_screen)
        
        # Verify that each star system's draw_galaxy_view method was called
        for system in mock_game.star_systems:
            system.draw_galaxy_view.assert_called_once_with(mock_screen)
    
    def test_draw_menu_state(self, galaxy_view, mock_game, mock_screen):
        """Test drawing in menu state."""
        # Set up mock game state
        mock_game.state = GameState.GALAXY_MENU
        mock_game.star_systems = [MagicMock(), MagicMock()]
        
        # Mock the background, panel, and menu draw methods
        mock_game.background.draw_galaxy_background = MagicMock()
        galaxy_view.panel.draw = MagicMock()
        galaxy_view.menu.draw = MagicMock()
        
        # Draw the view
        galaxy_view.draw(mock_screen)
        
        # Verify that the background, panel, and menu were drawn
        mock_game.background.draw_galaxy_background.assert_called_once_with(mock_screen)
        galaxy_view.panel.draw.assert_called_once_with(mock_screen)
        galaxy_view.menu.draw.assert_called_once_with(mock_screen)
        
        # Verify that each star system's draw_galaxy_view method was called
        for system in mock_game.star_systems:
            system.draw_galaxy_view.assert_called_once_with(mock_screen)

class TestGalaxyViewUpdate:
    """Tests for GalaxyView update method."""
    
    def test_update(self, galaxy_view):
        """Test the update method."""
        # The update method is empty, but we should test it for coverage
        galaxy_view.update()
        # If we got here without errors, the test passes
        assert True
