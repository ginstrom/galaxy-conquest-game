"""Tests for the PlanetView class."""

import pytest
import pygame
from unittest.mock import MagicMock, patch

from game.views.planet import PlanetView
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
def planet_view(mock_game, monkeypatch):
    """Create a PlanetView instance for testing."""
    # Mock the PlanetViewInfoPanel class to avoid pygame_gui initialization
    mock_panel = MagicMock()
    mock_panel.panel_width = 300
    
    # Create a mock class for PlanetViewInfoPanel
    MockPlanetViewInfoPanel = MagicMock(return_value=mock_panel)
    
    # Patch the PlanetViewInfoPanel import in planet.py
    monkeypatch.setattr('game.views.planet.PlanetViewInfoPanel', MockPlanetViewInfoPanel)
    
    # Now create the PlanetView instance
    view = PlanetView(mock_game)
    
    # Ensure the view has the mock panel
    view.panel = mock_panel
    
    return view

class TestPlanetViewInitialization:
    """Tests for PlanetView initialization."""
    
    def test_initialization(self, mock_game, monkeypatch):
        """Test that PlanetView initializes correctly."""
        # Mock the PlanetViewInfoPanel class to avoid pygame_gui initialization
        mock_panel = MagicMock()
        mock_panel.panel_width = 300
        
        # Create a mock class for PlanetViewInfoPanel
        MockPlanetViewInfoPanel = MagicMock(return_value=mock_panel)
        
        # Patch the PlanetViewInfoPanel import in planet.py
        monkeypatch.setattr('game.views.planet.PlanetViewInfoPanel', MockPlanetViewInfoPanel)
        
        # Now create the PlanetView instance
        view = PlanetView(mock_game)
        
        # Ensure the view has the mock panel
        view.panel = mock_panel
        
        assert view.game == mock_game
        assert view.panel is not None
        assert view.available_width == SCREEN_WIDTH - view.panel.panel_width
        assert view.center_x == view.available_width // 2
        assert view.center_y == SCREEN_HEIGHT // 2
        assert view.title_font is not None
        assert view.info_font is not None

class TestPlanetViewKeyHandling:
    """Tests for PlanetView key handling."""
    
    def test_handle_keydown_escape(self, planet_view, mock_game):
        """Test that pressing escape transitions to SYSTEM state."""
        # Create a mock event with escape key
        event = MagicMock()
        event.key = pygame.K_ESCAPE
        
        # Handle the key event
        planet_view.handle_keydown(event)
        
        # Verify that the selected planet is None and to_state was called
        assert mock_game.selected_planet is None
        mock_game.to_state.assert_called_once_with(GameState.PLANET, GameState.SYSTEM)
    
    def test_handle_keydown_other_key(self, planet_view, mock_game):
        """Test handling of non-escape keys."""
        # Set initial state
        mock_game.state = GameState.PLANET
        
        # Create a mock event with a non-escape key
        event = MagicMock()
        event.key = pygame.K_SPACE
        
        # Handle the key event
        planet_view.handle_keydown(event)
        
        # Verify that the game state did not change
        assert mock_game.state == GameState.PLANET

class TestPlanetViewMouseHandling:
    """Tests for PlanetView mouse handling."""
    
    def test_handle_click_in_info_panel(self, planet_view, mock_game):
        """Test handling of clicks in the info panel area."""
        # Position in the info panel area
        pos = (SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2)
        
        # Handle the click
        planet_view.handle_click(pos)
        
        # Verify that the game state did not change
        assert mock_game.state == GameState.PLANET
    
    def test_handle_click_in_planet_view(self, planet_view, mock_game):
        """Test handling of clicks in the planet view area."""
        # Position in the planet view area
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the click
        planet_view.handle_click(pos)
        
        # Verify that the selected planet is None and to_state was called
        assert mock_game.selected_planet is None
        mock_game.to_state.assert_called_once_with(GameState.PLANET, GameState.SYSTEM)
    
    def test_handle_right_click_in_info_panel(self, planet_view, mock_game):
        """Test handling of right clicks in the info panel area."""
        # Position in the info panel area
        pos = (SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2)
        
        # Handle the right click
        planet_view.handle_right_click(pos)
        
        # Verify that the game state did not change
        assert mock_game.state == GameState.PLANET
    
    def test_handle_right_click_in_planet_view(self, planet_view, mock_game):
        """Test handling of right clicks in the planet view area."""
        # Position in the planet view area
        pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Handle the right click
        planet_view.handle_right_click(pos)
        
        # Verify that the selected planet is None and to_state was called
        assert mock_game.selected_planet is None
        mock_game.to_state.assert_called_once_with(GameState.PLANET, GameState.SYSTEM)

class TestPlanetViewUpdate:
    """Tests for PlanetView update method."""
    
    def test_update(self, planet_view):
        """Test the update method."""
        # The update method is empty, but we should test it for coverage
        planet_view.update()
        # If we got here without errors, the test passes
        assert True

class TestPlanetViewDrawing:
    """Tests for PlanetView drawing."""
    
    @patch('pygame.draw.circle')
    def test_draw_with_selected_planet(self, mock_draw_circle, planet_view, mock_game, mock_screen):
        """Test drawing with a selected planet."""
        # Create mock font objects
        mock_title_font = MagicMock()
        mock_title_font.render.return_value = MockSurface((100, 30))
        mock_info_font = MagicMock()
        mock_info_font.render.return_value = MockSurface((100, 20))
        
        # Replace the real font objects with our mocks
        original_title_font = planet_view.title_font
        original_info_font = planet_view.info_font
        planet_view.title_font = mock_title_font
        planet_view.info_font = mock_info_font
        
        try:
            # Create a mock planet
            planet = {
                'name': 'Test Planet',
                'type': PlanetType.TERRESTRIAL,
                'size': 20,
                'resources': [
                    {'type': ResourceType.MINERALS, 'amount': 75},
                    {'type': ResourceType.WATER, 'amount': 50}
                ]
            }
            mock_game.selected_planet = planet
            
            # Mock the background and panel draw methods
            mock_game.background.draw_system_background = MagicMock()
            
            # Mock PlanetProperties.PROPERTIES to avoid KeyError
            with patch('game.views.planet.PlanetProperties.PROPERTIES', {
                PlanetType.TERRESTRIAL: {'color': (0, 255, 0)}
            }):
                # Draw the view
                planet_view.draw(mock_screen)
            
            # Verify that the background and panel were drawn
            mock_game.background.draw_system_background.assert_called_once_with(mock_screen)
            planet_view.panel.draw.assert_called_once_with(mock_screen)
            
            # Verify that pygame.draw.circle was called
            mock_draw_circle.assert_called_once()
        finally:
            # Restore the original font objects
            planet_view.title_font = original_title_font
            planet_view.info_font = original_info_font
    
    def test_draw_without_selected_planet(self, planet_view, mock_game, mock_screen):
        """Test drawing without a selected planet."""
        # Ensure no planet is selected
        mock_game.selected_planet = None
        
        # Draw the view
        planet_view.draw(mock_screen)
        
        # If we got here without errors, the test passes
        assert True
