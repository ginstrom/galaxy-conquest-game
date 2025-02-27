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

class MockSurface:
    """A mock surface that simulates pygame.Surface."""
    def __init__(self, size=(1, 1), flags=0):
        """Initialize with optional flags parameter."""
        if isinstance(size, (tuple, list)):
            self._size = size
        elif hasattr(size, 'size'):
            self._size = size.size
        else:
            self._size = (size[0], size[1])
        self._alpha = None
        self.flags = flags
        self._color = (0, 0, 0, 255)
        self._clip = None
        
    def convert(self):
        """Convert surface."""
        surf = MockSurface(self._size, self.flags)
        surf._color = self._color
        return surf
        
    def convert_alpha(self):
        """Convert surface with alpha."""
        surf = MockSurface(self._size, self.flags | pygame.SRCALPHA)
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
        rect = pygame.Rect(0, 0, self._size[0], self._size[1])
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
            source_size = source._size if hasattr(source, '_size') else source.get_size()
        return pygame.Rect(dest[0], dest[1], source_size[0], source_size[1])
        
    def fill(self, color, rect=None, special_flags=0):
        """Mock fill operation."""
        self._color = color
        
    def get_width(self):
        """Get surface width."""
        return self._size[0]
        
    def get_height(self):
        """Get surface height."""
        return self._size[1]
        
    def get_size(self):
        """Get surface size."""
        return self._size
        
    def get_at(self, pos):
        """Get color at position."""
        return (0, 0, 0, 255)  # Return black by default
        
    def copy(self):
        """Create a copy of the surface."""
        surf = MockSurface(self._size, self.flags)
        surf._color = self._color
        surf._alpha = self._alpha
        return surf

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


class MockUIElement:
    """Mock UI element for pygame_gui."""
    def __init__(self, relative_rect=None, text="", manager=None, container=None, object_id=None):
        self.relative_rect = relative_rect or pygame.Rect(0, 0, 100, 20)
        self.text = text
        self.manager = manager
        self.container = container
        self.object_id = object_id
        self.visible = True
        self.kill = MagicMock()
        self.set_text = MagicMock()
        self.set_position = MagicMock()
        self.set_dimensions = MagicMock()
        self.show = MagicMock()
        self.hide = MagicMock()

class MockUIPanel(MockUIElement):
    """Mock UI panel for pygame_gui."""
    pass

class MockUILabel(MockUIElement):
    """Mock UI label for pygame_gui."""
    pass

class MockUIHorizontalRule(MockUIElement):
    """Mock UI horizontal rule for pygame_gui."""
    pass

class MockContainer:
    """Mock container for pygame_gui."""
    def __init__(self, rect=None):
        self.rect = rect or pygame.Rect(0, 0, 800, 600)
        self.elements = []
        self.visible = 1
        
    def get_container(self):
        """Return self as the container."""
        return self
        
    def get_rect(self):
        """Return the container's rect."""
        return self.rect
        
    def get_abs_rect(self):
        """Return the container's absolute rect."""
        return self.rect
        
    def get_image_clipping_rect(self):
        """Return the container's image clipping rect."""
        return None
        
    def add_element(self, element):
        """Add an element to the container."""
        self.elements.append(element)

class MockTheme:
    """Mock theme for pygame_gui."""
    def __init__(self):
        # Create a shape_cache attribute with MagicMock
        self.shape_cache = MagicMock()
        # Add methods to shape_cache that might be called
        self.shape_cache.find_surface_in_cache = MagicMock(return_value=None)
        self.shape_cache.add_surface_to_cache = MagicMock()
        
    def build_all_combined_ids(self, element_ids, class_ids, object_ids):
        """Build all combined IDs."""
        # Return a non-empty list to avoid IndexError in UIPanel._create_valid_ids
        return ["panel"]
        
    def get_colour_or_gradient(self, colour_id, combined_ids=None):
        """Mock get_colour_or_gradient method."""
        # Return a default color (black)
        return (0, 0, 0, 255)
        
    def get_image(self, image_id, combined_ids=None):
        """Mock get_image method."""
        # Return None to indicate no image is available
        return None
        
    def get_misc_data(self, misc_data_id, combined_ids=None):
        """Mock get_misc_data method.
        
        This method is used by pygame_gui to get miscellaneous theme data like
        shape, border_width, shadow_width, etc.
        
        Args:
            misc_data_id: The ID of the miscellaneous data to get
            combined_ids: The combined IDs to use for the lookup
            
        Returns:
            A default value based on the requested data ID
        """
        # Return default values for common misc data IDs
        if misc_data_id == 'shape':
            return 'rectangle'
        elif misc_data_id == 'border_width':
            return 1
        elif misc_data_id == 'shadow_width':
            return 2
        elif misc_data_id == 'shape_corner_radius':
            return 2
        elif misc_data_id == 'text_horiz_alignment':
            return 'left'
        elif misc_data_id == 'text_vert_alignment':
            return 'top'
        elif misc_data_id == 'text_horiz_alignment_padding':
            return 0
        elif misc_data_id == 'text_vert_alignment_padding':
            return 0
        elif misc_data_id == 'tool_tip_delay':
            return 1.0
        elif misc_data_id == 'text_shadow_size':
            return 0
        elif misc_data_id == 'text_shadow_offset':
            return (0, 0)
        # Return a default value for any other misc data ID
        return None

class MockUIManager:
    """Mock UI manager for pygame_gui."""
    def __init__(self):
        self.process_events = MagicMock()
        self.update = MagicMock()
        self.draw_ui = MagicMock()
        self.theme = MockTheme()
        self.get_theme = MagicMock(return_value=self.theme)
        self.get_sprite_group = MagicMock(return_value=pygame.sprite.Group())
        self.clear_and_reset = MagicMock()
        self.set_visual_debug_mode = MagicMock()
        self.root_container = MockContainer(pygame.Rect(0, 0, 800, 600))
        
        # Create a MagicMock for the root container that will be returned by get_root_container
        # This ensures the returned object has a get_container method
        self.mock_root_container = MagicMock()
        # Make the get_container method of the mock return the actual root_container
        self.mock_root_container.get_container = MagicMock(return_value=self.root_container)
        # Set up get_root_container to return the mock_root_container
        self.get_root_container = MagicMock(return_value=self.mock_root_container)
        
        # Add get_shadow method
        self.get_shadow = MagicMock(return_value=MockSurface((100, 100)))

class MockGame:
    """Mock game class for testing planet view."""
    def __init__(self):
        # Initialize ui_manager first
        self.ui_manager = MockUIManager()
        
        self.startup_view = MagicMock()
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
        self.hovered_planet = None
        self.selected_system = MagicMock()
        self.selected_system.color = (255, 255, 255)
        self.selected_system.star_type.value = 'Test Type'
        
        # Initialize info_font, detail_font, and title_font
        self.info_font = MockFont()
        self.detail_font = MockFont()
        self.title_font = MockFont()
        
        # Initialize views after ui_manager
        self.galaxy_view = MagicMock()
        self.system_view = MagicMock()
        self.planet_view = MagicMock()
        
        # Initialize info_panel
        self.info_panel = MagicMock()
        
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

class MockInfoPanel:
    """Mock info panel class for testing
    planet view."""
    def __init__(self, game):
        self.panel_rect = pygame.Rect(0, 0, 300, 600)
        self.panel_width = 300
        self.game = game
        
        # Add pygame_gui elements
        self.ui_panel = MockUIPanel(
            relative_rect=self.panel_rect,
            manager=self.game.ui_manager
        )
        self.ui_elements = []
    
    def draw(self, screen):
        """Mock info panel drawing."""
        pass
        
    def clear_ui_elements(self):
        """Mock clear UI elements."""
        for element in self.ui_elements:
            element.kill()
        self.ui_elements = []
        
    def create_label(self, text, rect, font_size=None, text_color=None, is_title=False):
        """Mock create label."""
        label = MockUILabel(
            relative_rect=rect,
            text=text,
            manager=self.game.ui_manager,
            container=self.ui_panel
        )
        self.ui_elements.append(label)
        return label
        
    def create_horizontal_rule(self, y_position, padding=10):
        """Mock create horizontal rule."""
        rule_rect = pygame.Rect(
            padding, 
            y_position, 
            self.panel_width - (padding * 2), 
            2
        )
        rule = MockUIHorizontalRule(
            relative_rect=rule_rect,
            manager=self.game.ui_manager,
            container=self.ui_panel
        )
        self.ui_elements.append(rule)
        return rule
        
    def create_planet_details(self, planet, start_y):
        """Mock create planet details."""
        return start_y + 100  # Return a reasonable y-coordinate

class MockBackground:
    """Mock background class for testing."""
    def draw_system_background(self, screen):
        """Mock system background drawing."""
        pass
        
    def draw_galaxy_background(self, screen):
        """Mock galaxy background drawing."""
        pass
