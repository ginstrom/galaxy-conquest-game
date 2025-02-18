import pygame
from settings import DEBUG

class Debug:
    def __init__(self):
        self._font = None
        self._debug_info = []
        self._margin = 10
        self._line_height = 25
        self._bg_padding = 5
        self._enabled = DEBUG  # Initialize with settings value
    
    def toggle(self):
        """Toggle debug display on/off."""
        self._enabled = not self._enabled
        if not self._enabled:
            self.clear()
    
    @property
    def enabled(self):
        """Get current debug state."""
        return self._enabled
    
    def _ensure_font_initialized(self):
        """Ensure the font is initialized when needed."""
        if self._font is None and self._enabled:
            self._font = pygame.font.Font(None, 24)
    
    def clear(self):
        """Clear all debug information for the current frame."""
        if self._enabled:
            self._debug_info.clear()
    
    def add(self, info, color=(255, 255, 255), pos=None):
        """
        Add debug information to be displayed.
        
        Args:
            info: String or value to display
            color: RGB tuple for text color (default: white)
            pos: Optional (x, y) position. If None, will be added to list
        """
        if self._enabled:
            self._debug_info.append({
                'text': str(info),
                'color': color,
                'pos': pos
            })
    
    def draw(self, surface):
        """
        Draw all debug information to the surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self._enabled:
            return
            
        self._ensure_font_initialized()
        y = self._margin
        
        for info in self._debug_info:
            text_surface = self._font.render(info['text'], True, info['color'])
            text_rect = text_surface.get_rect()
            
            if info['pos'] is None:
                # Default position on left side
                text_rect.topleft = (self._margin, y)
                y += self._line_height
            else:
                # Custom position
                text_rect.topleft = info['pos']
            
            # Draw background rectangle
            bg_rect = text_rect.inflate(self._bg_padding * 2, self._bg_padding * 2)
            pygame.draw.rect(surface, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(surface, (128, 128, 128), bg_rect, 1)
            
            # Draw text
            surface.blit(text_surface, text_rect)

# Global debug instance
_debug = Debug()

def debug(info, color=(255, 255, 255), pos=None):
    """
    Add debug information to be displayed on screen.
    If debug is disabled, this function becomes a no-op.
    
    Args:
        info: String or value to display
        color: RGB tuple for text color (default: white)
        pos: Optional (x, y) position. If None, will be added to list
    """
    if not is_debug_enabled():
        return
    _debug.add(info, color, pos)

def clear_debug():
    """Clear all debug information for the current frame."""
    _debug.clear()

def draw_debug(surface):
    """
    Draw all debug information to the surface.
    If debug is disabled, this function becomes a no-op.
    
    Args:
        surface: Pygame surface to draw on
    """
    _debug.draw(surface)

def toggle_debug():
    """Toggle debug display on/off."""
    _debug.toggle()

def is_debug_enabled():
    """Get current debug state."""
    return _debug.enabled
