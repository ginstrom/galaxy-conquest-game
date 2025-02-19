"""Test configuration and fixtures."""
import pytest
from unittest.mock import Mock
from tests.mocks import MockPygame, MockSurface
from game.resources import ResourceManager

@pytest.fixture(scope="function")
def mock_pygame():
    """Create a mock pygame instance."""
    return MockPygame()

@pytest.fixture(scope="function")
def resource_manager(mock_pygame):
    """Create a ResourceManager instance with mock pygame modules."""
    manager = ResourceManager(
        pygame_module=mock_pygame,
        font_module=mock_pygame.font,
        mixer_module=mock_pygame.mixer,
        display_module=mock_pygame.display
    )
    yield manager
    manager.cleanup()

@pytest.fixture
def mock_game(resource_manager):
    """Create a mock game instance for testing."""
    game = Mock()
    game.screen = MockSurface((800, 600))
    game.resource_manager = resource_manager
    return game