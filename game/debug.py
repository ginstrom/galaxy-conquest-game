import pygame
import pygame_gui
from settings import DEBUG

class Debug:
    def __init__(self, ui_manager=None):
        self._font = None
        self._debug_info = []
        self._margin = 10
        self._line_height = 25
        self._bg_padding = 5
        self._enabled = DEBUG  # Initialize with settings value
        self._console_visible = False
        self._ui_manager = ui_manager
        self._console_initialized = False
        self._console_height = 200  # Height of the console area
        self._console_input = None
        self._console_output = None
    
    def set_ui_manager(self, ui_manager):
        """Set the UI manager for the debug console."""
        self._ui_manager = ui_manager
        self._initialize_console()
    
    def _initialize_console(self):
        """Initialize the console UI elements."""
        if self._ui_manager and not self._console_initialized:
            screen_width = pygame.display.get_surface().get_width()
            
            # Create console input line at the bottom of the console area
            self._console_input = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((0, self._console_height - 30), (screen_width, 30)),
                manager=self._ui_manager,
                visible=False
            )
            
            # Create console output box above the input line
            self._console_output = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((0, 0), (screen_width, self._console_height - 30)),
                html_text="<font color='#00FF00'>Debug Console</font><br>Type 'help' for available commands",
                manager=self._ui_manager,
                visible=False
            )
            
            self._console_initialized = True
    
    def toggle(self):
        """Toggle debug display on/off."""
        self._enabled = not self._enabled
        if not self._enabled:
            self.clear()
            self.hide_console()
    
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
    
    def toggle_console(self):
        """Toggle the debug console visibility."""
        if not self._console_initialized and self._ui_manager:
            self._initialize_console()
            
        if self._console_initialized:
            if self._console_visible:
                self.hide_console()
            else:
                self.show_console()
    
    def show_console(self):
        """Show the debug console."""
        if self._console_initialized:
            self._console_visible = True
            self._console_input.show()
            self._console_output.show()
            # Set focus to the input line
            self._console_input.focus()
    
    def hide_console(self):
        """Hide the debug console."""
        if self._console_initialized:
            self._console_visible = False
            self._console_input.hide()
            self._console_output.hide()
    
    def handle_event(self, event):
        """
        Handle events for the debug console.
        
        Args:
            event: Pygame event to handle
        
        Returns:
            bool: True if the event was handled by the console, False otherwise
        """
        if not self._console_initialized:
            return False
            
        # Toggle console with backtick key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                self.toggle_console()
                return True
            elif event.key == pygame.K_ESCAPE and self._console_visible:
                self.hide_console()
                return True
        
        # Handle console input
        if self._console_visible and event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == self._console_input:
            command = self._console_input.get_text()
            self._process_command(command)
            self._console_input.set_text("")
            return True
            
        return False
    
    def _process_command(self, command):
        """
        Process a command entered in the console.
        
        Args:
            command: Command string to process
        """
        if not command.strip():
            return
            
        # Add command to output
        self._add_to_console(f"> {command}")
        
        # Process command
        cmd_parts = command.strip().split()
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1:] if len(cmd_parts) > 1 else []
        
        if cmd == "help":
            self._add_to_console("Available commands:")
            self._add_to_console("  help - Show this help")
            self._add_to_console("  clear - Clear the console")
            self._add_to_console("  toggle - Toggle debug display")
        elif cmd == "clear":
            self._clear_console()
        elif cmd == "toggle":
            self.toggle()
            self._add_to_console(f"Debug display: {'ON' if self._enabled else 'OFF'}")
        else:
            self._add_to_console(f"Unknown command: {cmd}")
    
    def _add_to_console(self, text):
        """
        Add text to the console output.
        
        Args:
            text: Text to add to the console
        """
        if self._console_output:
            current_text = self._console_output.html_text
            self._console_output.html_text = f"{current_text}<br><font color='#FFFFFF'>{text}</font>"
            self._console_output.rebuild()
    
    def _clear_console(self):
        """Clear the console output."""
        if self._console_output:
            self._console_output.html_text = "<font color='#00FF00'>Debug Console</font><br>Type 'help' for available commands"
            self._console_output.rebuild()
    
    def draw(self, surface):
        """
        Draw all debug information to the surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self._enabled or self._console_visible:
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

def set_ui_manager(ui_manager):
    """
    Set the UI manager for the debug console.
    
    Args:
        ui_manager: pygame_gui UIManager instance
    """
    _debug.set_ui_manager(ui_manager)

def handle_debug_event(event):
    """
    Handle events for the debug console.
    
    Args:
        event: Pygame event to handle
        
    Returns:
        bool: True if the event was handled by the console, False otherwise
    """
    return _debug.handle_event(event)

def toggle_console():
    """Toggle the debug console visibility."""
    _debug.toggle_console()

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
