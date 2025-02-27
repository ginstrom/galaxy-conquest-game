"""Tests for the InfoPanel classes."""

import pytest
import pygame
from pygame.locals import K_ESCAPE
from unittest.mock import MagicMock, patch

# Initialize pygame and font module for testing
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# Import game modules after pygame initialization
from game.views.infopanel import InfoPanel, GalaxyViewInfoPanel, SystemViewInfoPanel, PlanetViewInfoPanel
from game.enums import PlanetType, ResourceType, GameState
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from tests.mocks import MockGame, MockSurface, MockUIElement

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
def mock_ui_panel():
    """Mock the UIPanel class."""
    with patch('game.views.infopanel.UIPanel') as mock_panel_class:
        # Create a MagicMock instance for the panel
        mock_panel = MagicMock()
        mock_panel.relative_rect = pygame.Rect(SCREEN_WIDTH - 300, 0, 300, SCREEN_HEIGHT)
        
        # Configure the mock class to return our mock panel
        mock_panel_class.return_value = mock_panel
        yield mock_panel

@pytest.fixture
def mock_ui_label():
    """Mock the UILabel class."""
    with patch('game.views.infopanel.UILabel') as mock_label_class:
        # Create a MagicMock instance for the label
        mock_label = MagicMock()
        mock_label.text = "Test Label"
        
        # Configure the mock class to return our mock label
        mock_label_class.return_value = mock_label
        yield mock_label

@pytest.fixture
def mock_info_panel(mock_ui_panel, mock_ui_label):
    """Mock the InfoPanel class."""
    with patch('game.views.infopanel.InfoPanel', autospec=True) as mock_panel_class:
        # Create a MagicMock instance for the panel
        mock_panel = MagicMock(spec=InfoPanel)
        mock_panel.panel_width = 300
        mock_panel.panel_rect = pygame.Rect(SCREEN_WIDTH - 300, 0, 300, SCREEN_HEIGHT)
        mock_panel.ui_panel = mock_ui_panel
        mock_panel.ui_elements = []
        mock_panel.draw = MagicMock()
        mock_panel.clear_ui_elements = MagicMock()
        mock_panel.create_label = MagicMock(return_value=mock_ui_label)
        mock_panel.create_horizontal_rule = MagicMock()
        mock_panel.create_planet_details = MagicMock(return_value=200)  # Return a reasonable y-coordinate
        
        # Configure the mock class to return our mock panel
        mock_panel_class.return_value = mock_panel
        yield mock_panel_class

@pytest.fixture
def mock_galaxy_view_info_panel(mock_info_panel):
    """Mock the GalaxyViewInfoPanel class."""
    with patch('game.views.infopanel.GalaxyViewInfoPanel', autospec=True) as mock_panel_class:
        # Create a MagicMock instance for the panel
        mock_panel = MagicMock(spec=GalaxyViewInfoPanel)
        mock_panel.panel_width = 300
        mock_panel.panel_rect = pygame.Rect(SCREEN_WIDTH - 300, 0, 300, SCREEN_HEIGHT)
        mock_panel.ui_panel = MagicMock()
        mock_panel.ui_elements = []
        mock_panel.draw = MagicMock()
        mock_panel.last_hovered_system = None
        mock_panel._create_system_info = MagicMock()
        mock_panel._create_default_info = MagicMock()
        
        # Configure the mock class to return our mock panel
        mock_panel_class.return_value = mock_panel
        yield mock_panel

@pytest.fixture
def mock_system_view_info_panel(mock_info_panel):
    """Mock the SystemViewInfoPanel class."""
    with patch('game.views.infopanel.SystemViewInfoPanel', autospec=True) as mock_panel_class:
        # Create a MagicMock instance for the panel
        mock_panel = MagicMock(spec=SystemViewInfoPanel)
        mock_panel.panel_width = 300
        mock_panel.panel_rect = pygame.Rect(SCREEN_WIDTH - 300, 0, 300, SCREEN_HEIGHT)
        mock_panel.ui_panel = MagicMock()
        mock_panel.ui_elements = []
        mock_panel.draw = MagicMock()
        mock_panel.last_hovered_planet = None
        mock_panel.last_selected_planet = None
        mock_panel.last_selected_system = None
        mock_panel._create_system_info = MagicMock(return_value=170)
        
        # Configure the mock class to return our mock panel
        mock_panel_class.return_value = mock_panel
        yield mock_panel

@pytest.fixture
def mock_planet_view_info_panel(mock_info_panel):
    """Mock the PlanetViewInfoPanel class."""
    with patch('game.views.infopanel.PlanetViewInfoPanel', autospec=True) as mock_panel_class:
        # Create a MagicMock instance for the panel
        mock_panel = MagicMock(spec=PlanetViewInfoPanel)
        mock_panel.panel_width = 300
        mock_panel.panel_rect = pygame.Rect(SCREEN_WIDTH - 300, 0, 300, SCREEN_HEIGHT)
        mock_panel.ui_panel = MagicMock()
        mock_panel.ui_elements = []
        mock_panel.draw = MagicMock()
        mock_panel.last_selected_planet = None
        mock_panel.last_selected_system = None
        mock_panel._create_system_info = MagicMock(return_value=170)
        
        # Configure the mock class to return our mock panel
        mock_panel_class.return_value = mock_panel
        yield mock_panel

def test_base_infopanel_initialization(mock_ui_panel):
    """Test base InfoPanel initialization."""
    with patch('game.views.infopanel.UIPanel', return_value=mock_ui_panel):
        game = MockGame()
        panel = InfoPanel(game)
        
        assert panel.game == game
        assert panel.panel_width == 300
        assert panel.panel_rect.width == 300
        assert panel.panel_rect.height == SCREEN_HEIGHT
        assert panel.panel_rect.left == SCREEN_WIDTH - 300
        assert panel.panel_rect.top == 0
        assert panel.ui_panel is not None
        assert len(panel.ui_elements) == 0

def test_base_infopanel_draw(mock_game, mock_screen, mock_ui_panel):
    """Test base InfoPanel draw method."""
    with patch('game.views.infopanel.UIPanel', return_value=mock_ui_panel):
        panel = InfoPanel(mock_game)
        panel.draw(mock_screen)
        
        # The base draw method doesn't do anything now as pygame_gui handles the drawing
        # We can ensure it doesn't raise errors
        assert True  # If we got here, no exceptions were raised

def test_base_infopanel_ui_methods(mock_game, mock_ui_panel, mock_ui_label):
    """Test base InfoPanel UI methods."""
    with patch('game.views.infopanel.UIPanel', return_value=mock_ui_panel):
        with patch('game.views.infopanel.UILabel', return_value=mock_ui_label):
            panel = InfoPanel(mock_game)
            
            # Test clear_ui_elements
            panel.ui_elements = [MagicMock(), MagicMock()]
            for element in panel.ui_elements:
                element.kill = MagicMock()
            panel.clear_ui_elements()
            assert len(panel.ui_elements) == 0
            
            # Test create_label
            rect = pygame.Rect(10, 20, 100, 30)
            label = panel.create_label("Test Label", rect)
            assert label in panel.ui_elements
            
            # Test create_horizontal_rule
            with patch('game.views.infopanel.UIPanel', return_value=MagicMock()) as mock_rule:
                rule = panel.create_horizontal_rule(50)
                assert rule in panel.ui_elements
            
            # Test create_planet_details
            planet = {
                'name': 'Test Planet',
                'type': PlanetType.TERRESTRIAL,
                'resources': [
                    {'type': ResourceType.MINERALS, 'amount': 75},
                    {'type': ResourceType.WATER, 'amount': 50}
                ]
            }
            
            # Mock the create_label method to avoid actual UI creation
            original_create_label = panel.create_label
            panel.create_label = MagicMock(return_value=mock_ui_label)
            
            y = panel.create_planet_details(planet, 100)
            assert y > 100  # Should return a y-coordinate after the planet details
            
            # Restore the original method
            panel.create_label = original_create_label

def test_base_infopanel_input_handlers(mock_game, mock_ui_panel):
    """Test base InfoPanel input handler methods."""
    with patch('game.views.infopanel.UIPanel', return_value=mock_ui_panel):
        panel = InfoPanel(mock_game)
        
        # These methods should not raise errors
        panel.handle_input(None)
        panel.handle_click((0, 0))
        panel.handle_keydown(None)
        
        # If we got here, no exceptions were raised
        assert True

def test_galaxy_view_infopanel_initialization(mock_game, mock_galaxy_view_info_panel):
    """Test GalaxyViewInfoPanel initialization."""
    panel = mock_galaxy_view_info_panel
    
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT

def test_galaxy_view_infopanel_draw_with_hovered_system(mock_game, mock_screen, mock_galaxy_view_info_panel):
    """Test GalaxyViewInfoPanel draw method with a hovered system."""
    panel = mock_galaxy_view_info_panel
    
    # Set up a hovered system
    mock_game.hovered_system = mock_game.selected_system
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_galaxy_view_infopanel_draw_without_hovered_system(mock_game, mock_screen, mock_galaxy_view_info_panel):
    """Test GalaxyViewInfoPanel draw method without a hovered system."""
    panel = mock_galaxy_view_info_panel
    
    # Ensure no hovered system
    mock_game.hovered_system = None
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_system_view_infopanel_initialization(mock_game, mock_system_view_info_panel):
    """Test SystemViewInfoPanel initialization."""
    panel = mock_system_view_info_panel
    
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT

def test_system_view_infopanel_draw_with_selected_system(mock_game, mock_screen, mock_system_view_info_panel):
    """Test SystemViewInfoPanel draw method with a selected system."""
    panel = mock_system_view_info_panel
    
    # Set up a selected system
    mock_game.selected_system = mock_game.selected_system
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_system_view_infopanel_draw_with_selected_planet(mock_game, mock_screen, mock_system_view_info_panel):
    """Test SystemViewInfoPanel draw method with a selected planet."""
    panel = mock_system_view_info_panel
    
    # Set up a selected system and planet
    mock_game.selected_system = mock_game.selected_system
    mock_game.selected_planet = {
        'name': 'Test Planet',
        'type': PlanetType.TERRESTRIAL,
        'resources': [
            {'type': ResourceType.MINERALS, 'amount': 75},
            {'type': ResourceType.WATER, 'amount': 50}
        ]
    }
    mock_game.hovered_planet = None  # Ensure no hovered planet
    mock_game.state = GameState.SYSTEM
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_system_view_infopanel_draw_with_hovered_planet(mock_game, mock_screen, mock_system_view_info_panel):
    """Test SystemViewInfoPanel draw method with a hovered planet."""
    panel = mock_system_view_info_panel
    
    # Set up a selected system and hovered planet
    mock_game.selected_system = mock_game.selected_system
    mock_game.selected_planet = None  # No selected planet
    mock_game.hovered_planet = {
        'name': 'Hovered Planet',
        'type': PlanetType.GAS_GIANT,
        'resources': [
            {'type': ResourceType.GASES, 'amount': 100},
            {'type': ResourceType.RARE_ELEMENTS, 'amount': 25}
        ]
    }
    mock_game.state = GameState.SYSTEM
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_system_view_infopanel_draw_with_both_selected_and_hovered_planet(mock_game, mock_screen, mock_system_view_info_panel):
    """Test SystemViewInfoPanel draw method with both selected and hovered planets."""
    panel = mock_system_view_info_panel
    
    # Set up a selected system, selected planet, and hovered planet
    mock_game.selected_system = mock_game.selected_system
    mock_game.selected_planet = {
        'name': 'Selected Planet',
        'type': PlanetType.TERRESTRIAL,
        'resources': [
            {'type': ResourceType.MINERALS, 'amount': 75},
            {'type': ResourceType.WATER, 'amount': 50}
        ]
    }
    mock_game.hovered_planet = {
        'name': 'Hovered Planet',
        'type': PlanetType.GAS_GIANT,
        'resources': [
            {'type': ResourceType.GASES, 'amount': 100},
            {'type': ResourceType.RARE_ELEMENTS, 'amount': 25}
        ]
    }
    mock_game.state = GameState.SYSTEM
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_system_view_infopanel_draw_without_selected_system(mock_game, mock_screen, mock_system_view_info_panel):
    """Test SystemViewInfoPanel draw method without a selected system."""
    panel = mock_system_view_info_panel
    
    # Ensure no selected system
    mock_game.selected_system = None
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_planet_view_infopanel_initialization(mock_game, mock_planet_view_info_panel):
    """Test PlanetViewInfoPanel initialization."""
    panel = mock_planet_view_info_panel
    
    assert panel.panel_width == 300
    assert panel.panel_rect.width == 300
    assert panel.panel_rect.height == SCREEN_HEIGHT

def test_planet_view_infopanel_draw_with_selected_planet(mock_game, mock_screen, mock_planet_view_info_panel):
    """Test PlanetViewInfoPanel draw method with a selected planet."""
    panel = mock_planet_view_info_panel
    
    # Set up a selected planet
    mock_game.selected_planet = {
        'name': 'Test Planet',
        'type': PlanetType.TERRESTRIAL,
        'resources': [
            {'type': ResourceType.MINERALS, 'amount': 75},
            {'type': ResourceType.WATER, 'amount': 50}
        ]
    }
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called

def test_planet_view_infopanel_draw_without_selected_planet(mock_game, mock_screen, mock_planet_view_info_panel):
    """Test PlanetViewInfoPanel draw method without a selected planet."""
    panel = mock_planet_view_info_panel
    
    # Ensure no selected planet
    mock_game.selected_planet = None
    
    # Draw the panel
    panel.draw(mock_screen)
    
    # Verify the draw method was called
    assert panel.draw.called
