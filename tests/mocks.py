"""Mock implementations for pygame objects and modules."""
from unittest.mock import MagicMock, Mock
import pygame
import os
from game.enums import PlanetType, ResourceType, GameState

class MockFont:
    def __init__(self, name=None, size=None):
        self.name = name
        self.size = size if size is not None else 24  # Default size to 24 if None

    def render(self, text, antialias, color):
        return MockSurface((len(text) * self.size // 2, self.size))

class MockSurface(pygame.Surface):
    """A mock surface that extends pygame.Surface."""
    def __init__(self, size=(1, 1), flags=0):
        """Initialize with optional flags parameter."""
        if isinstance(size, (tuple, list)):
            self.size = size
        elif hasattr(size, 'size'):
            self.size = size.size
        else:
            self.size = (size[0], size[1])
        super().__init__(self.size, flags)
        self._alpha = None
        self.flags = flags
        self._color = (0, 0, 0, 255)
        self._clip = None
        
    def convert(self):
        """Convert surface."""
        surf = MockSurface(self.size, self.flags)
        surf._color = self._color
        return surf
        
    def convert_alpha(self):
        """Convert surface with alpha."""
        surf = MockSurface(self.size, self.flags | pygame.SRCALPHA)
        surf._alpha = 255
        surf._color = self._color
        return surf
        
    def get_alpha(self):
        """Get alpha value."""
        return self._alpha
        
    def set_alpha(self, alpha):
        """Set alpha value."""
        self._alpha = alpha
        
    def get_rect(self, **kwargs):
        """Get the rectangle for this surface."""
        rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        for key, value in kwargs.items():
            if key == 'center':
                rect.centerx = value[0]
                rect.centery = value[1]
            else:
                setattr(rect, key, value)
        return rect
        
    def blit(self, source, dest, area=None, special_flags=0):
        """Mock blit operation."""
        if isinstance(dest, (pygame.Rect, MockSurface)):
            return dest
        if isinstance(source, pygame.Surface):
            source_size = source.get_size()
        else:
            source_size = source.size
        return pygame.Rect(dest[0], dest[1], source_size[0], source_size[1])
        
    def fill(self, color, rect=None, special_flags=0):
        """Mock fill operation."""
        self._color = color
        
    def get_width(self):
        """Get surface width."""
        return self.size[0]
        
    def get_height(self):
        """Get surface height."""
        return self.size[1]
        
    def get_size(self):
        """Get surface size."""
        return self.size
        
    def get_at(self, pos):
        """Get color at position."""
        return (0, 0, 0, 255)  # Return black by default

class MockSound:
    def __init__(self, buffer=None):
        self.buffer = buffer
        self.playing = False
        
    def play(self):
        self.playing = True
        
    def stop(self):
        self.playing = False

class MockPygame:
    def __init__(self):
        # Initialize pygame for testing
        if not pygame.get_init():
            pygame.init()
            pygame.font.init()
            pygame.mixer.init()
            
        self.init_called = False
        self.quit_called = False
        self.font = MagicMock()
        self.mixer = MagicMock()
        self.display = MagicMock()
        self.error = pygame.error
        self.time = pygame.time
        
        # Setup Surface with flags support
        def mock_surface(*args, **kwargs):
            if len(args) == 1:
                size = args[0]
            elif len(args) == 2:
                size = args[0]
            else:
                size = kwargs.get('size', (1, 1))
            flags = kwargs.get('flags', 0)
            if len(args) >= 2:
                flags = args[1]
            return MockSurface(size, flags)
        self.Surface = mock_surface
        self.SRCALPHA = 0x00010000
        
        self.image = MagicMock()
        self.draw = MagicMock()
        
        # Setup draw module
        def mock_circle(surface, color, pos, radius, width=0):
            rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
            if isinstance(surface, (pygame.Surface, MockSurface)):
                if hasattr(surface, '_color'):
                    surface._color = color
            return rect
            
        def mock_rect(surface, color, rect, width=0):
            if isinstance(surface, (pygame.Surface, MockSurface)):
                if hasattr(surface, '_color'):
                    surface._color = color
            return rect if isinstance(rect, pygame.Rect) else pygame.Rect(rect)
            
        def mock_line(surface, color, start_pos, end_pos, width=1):
            if isinstance(surface, (pygame.Surface, MockSurface)):
                if hasattr(surface, '_color'):
                    surface._color = color
            return pygame.Rect(
                min(start_pos[0], end_pos[0]),
                min(start_pos[1], end_pos[1]),
                abs(end_pos[0] - start_pos[0]) or 1,
                abs(end_pos[1] - start_pos[1]) or 1
            )
            
        self.draw = pygame.draw
        self.draw.circle = mock_circle
        self.draw.rect = mock_rect
        self.draw.line = mock_line
        
        # Setup image module
        def mock_load(path):
            if not os.path.exists(path):
                raise FileNotFoundError(f"No such file: {path}")
            return MockSurface((32, 32))
        self.image.load = mock_load
        
        # Setup font module
        self.font.Font = MockFont
        self.font.SysFont = MockFont
        self.font.get_init = lambda: True
        self.font.init = lambda: None
        
        # Setup mixer module
        def mock_sound(path=None, buffer=None):
            if path is not None and not os.path.exists(path):
                raise FileNotFoundError(f"No such file: {path}")
            return MockSound(buffer)
        self.mixer.Sound = mock_sound
        self.mixer.get_init = lambda: True
        self.mixer.init = lambda *args, **kwargs: None
        
        # Setup display module
        self.display.get_init = lambda: True
        self.display.init = lambda: None
        self.display.set_mode = lambda *args, **kwargs: MockSurface((800, 600))
        
    def init(self):
        self.init_called = True
        
    def quit(self):
        self.quit_called = True
        
    def get_init(self):
        return self.init_called


class MockInfoPanel:
    """Mock info panel class for testing
    planet view."""
    def __init__(self, game):
        self.panel_rect = pygame.Rect(0, 0, 300, 600)
        self.panel_width = 300
        self.game = game
        self.game.selected_system = MagicMock()
        self.game.state = GameState.SYSTEM
        self.game.selected_planet = {
            'name': 'Test Planet',
            'type': PlanetType.TERRESTRIAL,
            'resources': [
                {'type': ResourceType.MINERALS, 'amount': 75},
                {'type': ResourceType.WATER, 'amount': 50}
            ]
        }
        self.game.info_font = MockFont()
        self.game.detail_font = MockFont()
        self.game.title_font = MockFont()
        self.game.selected_system.color = (255, 255, 255)
        self.game.selected_system.star_type.value = 'Test Type'
    
    def draw(self, screen):
        """Mock info panel drawing."""
        pass

class MockGame:
    """Mock game class for testing planet view."""
    def __init__(self):
        self.startup_view = MagicMock()
        self.galaxy_view = MagicMock()
        self.galaxy_view.panel = MockInfoPanel(self)
        self.system_view = MagicMock()
        self.system_view.panel = MockInfoPanel(self)
        self.planet_view = MagicMock()
        self.planet_view.panel = MockInfoPanel(self)
        self.info_panel = MockInfoPanel(self)  # Add info_panel attribute
        self.selected_planet = {
            'name': 'Test Planet',
            'type': PlanetType.TERRESTRIAL,
            'size': 10,
            'orbit_number': 1,
            'resources': [
                {'type': ResourceType.MINERALS, 'amount': 75},
                {'type': ResourceType.WATER, 'amount': 50}
            ]
        }
        self.background = MockBackground()
        self.state = GameState.PLANET
        self.star_systems = []
        self.hovered_system = None
        
        # Add methods needed for view initialization
        self.new_game = MagicMock(return_value=True)
        self.save_game = MagicMock(return_value=True)
        self.return_to_game = MagicMock(return_value=True)
        self.quit_to_main_menu = MagicMock(return_value=True)
        self.quit_game = MagicMock(return_value=True)
        self.go_to_galaxy_view = MagicMock(return_value=True)
        
    def draw_info_panel(self, screen):
        """Mock info panel drawing."""
        pass

class MockBackground:
    """Mock background class for testing."""
    def draw_system_background(self, screen):
        """Mock system background drawing."""
        pass
        
    def draw_galaxy_background(self, screen):
        """Mock galaxy background drawing."""
        pass
